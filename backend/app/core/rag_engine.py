import os
import PyPDF2  # For reading PDFs
from langchain_chroma import Chroma  # The vector database
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter  # For "chunking"
# from langchain_openai import OpenAIEmbeddings  # For creating embeddings

# Import our API key from the config file
# from app.core.config import OPENAI_API_KEY

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GOOGLE_API_KEY

# Set the OpenAI API key for the LangChain library
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Define the path for our persistent vector store
CHROMA_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'vector_store')

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a given PDF file.

    Args:
        pdf_path: The file path to the PDF.

    Returns:
        A single string containing all the text from the PDF.
    """
    print(f"Extracting text from: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() or ""
        print(f"Text extraction successful. Total characters: {len(full_text)}")
        return full_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def get_text_chunks(full_text: str) -> list[str]:
    """
    Splits a large text string into smaller "chunks".

    Args:
        full_text: The complete text string from the document.

    Returns:
        A list of smaller text strings (chunks).
    """
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Aim for chunks of 1000 characters
        chunk_overlap=200, # Each chunk overlaps the previous one by 200 characters
        length_function=len
    )
    chunks = text_splitter.split_text(full_text)
    print(f"Text split into {len(chunks)} chunks.")
    return chunks


def create_and_store_embeddings(chunks: list[str]):
    """
    Converts text chunks into embeddings and stores them in ChromaDB.
    """
    print("Initializing Google embeddings model...")
    # Initialize the embeddings model
    # embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    print(f"Initializing ChromaDB at: {CHROMA_DB_PATH}")
    # Initialize ChromaDB in "persistent" mode
    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings_model
    )

    print(f"Adding {len(chunks)} chunks to vector store...")
    # This is the "magic" step. LangChain handles:
    # 1. Taking each chunk
    # 2. Sending it to OpenAI to get an embedding
    # 3. Adding the text and its embedding to ChromaDB
    vector_store.add_texts(texts=chunks)
    
    # Ensure the data is saved to disk
    # vector_store.persist()
    print("Embeddings created and stored successfully.")


def process_document(pdf_path: str):
    """
    The main "Ingestion" pipeline.
    Orchestrates the entire process of reading, chunking, and storing a document.
    """
    print(f"Starting ingestion pipeline for {pdf_path}...")
    
    # Step 1: Extract text
    document_text = extract_text_from_pdf(pdf_path)
    if not document_text:
        print("Text extraction failed. Aborting pipeline.")
        return

    # Step 2: Split into chunks
    text_chunks = get_text_chunks(document_text)
    if not text_chunks:
        print("Text chunking failed. Aborting pipeline.")
        return

    # Step 3: Create and store embeddings
    create_and_store_embeddings(text_chunks)
    
    print(f"Successfully processed and indexed {pdf_path}")