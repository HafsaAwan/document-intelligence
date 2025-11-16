import os
import shutil
from fastapi import APIRouter, HTTPException

# Get the path to the vector store from our engine
from app.core.rag_engine import CHROMA_DB_PATH

router = APIRouter()

@router.post("/reset")
async def http_reset_vector_store():
    """
    Deletes the entire vector_store directory.
    This is a dangerous operation and should be used with caution.
    """
    print(f"--- RESET REQUEST RECEIVED ---")
    try:
        if os.path.exists(CHROMA_DB_PATH):
            print(f"Deleting vector store at: {CHROMA_DB_PATH}")
            shutil.rmtree(CHROMA_DB_PATH)
            # Re-create the empty directory
            os.makedirs(CHROMA_DB_PATH, exist_ok=True)
            print("Vector store has been reset.")
            return {"message": "Vector store has been successfully reset."}
        else:
            print("Vector store not found, nothing to delete.")
            return {"message": "Vector store not found, nothing to delete."}
            
    except Exception as e:
        print(f"Error resetting vector store: {e}")
        raise HTTPException(status_code=500, detail=f"Error resetting vector store: {e}")