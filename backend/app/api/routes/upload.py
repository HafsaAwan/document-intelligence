import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

# Import our RAG engine's main processing function
from app.core.rag_engine import process_document

# Define the path where uploaded files will be saved
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'uploads')

# Create the router
router = APIRouter()

@router.post("/upload")
async def http_upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF document.
    It saves the file and then processes it using the RAG engine.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided.")
        
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Create a safe file path
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    print(f"Saving uploaded file to: {file_path}")
    try:
        # Save the uploaded file to disk
        # We use 'shutil.copyfileobj' for an efficient file copy
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    finally:
        # Always close the file
        file.file.close()

    try:
        # Now, process the document we just saved
        print(f"File saved. Starting RAG processing for: {file_path}")
        process_document(file_path)
    except Exception as e:
        print(f"Error during RAG processing: {e}")
        # Note: If this fails, the file is saved but not indexed.
        raise HTTPException(status_code=500, detail=f"File saved, but error during processing: {e}")
        
    return {"message": "File uploaded and processed successfully.", "filename": file.filename}