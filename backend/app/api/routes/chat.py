from fastapi import APIRouter, HTTPException
from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
# from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GOOGLE_API_KEY
# Import our schema and config
from app.models.schemas import ChatRequest
# from app.core.config import OPENAI_API_KEY
from app.core.rag_engine import CHROMA_DB_PATH # Import the path from our engine

# Create the router
router = APIRouter()

# --- Define RAG Chain components ---

# 1. Initialize Embeddings Model (must be same as ingestion)
# embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# 2. Load the persistent vector store
try:
    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings_model
    )
    # Create the "retriever"
    retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 chunks
    print("ChromaDB loaded successfully.")
except Exception as e:
    print(f"Error loading ChromaDB: {e}")
    # If DB fails to load, the chat endpoint is useless
    retriever = None

# 3. Define the Prompt Template
template = """
You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.

Context: {context} 

Question: {question} 

Helpful Answer:
"""
rag_prompt = PromptTemplate.from_template(template)

# 4. Initialize the LLM
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=OPENAI_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2, google_api_key=GOOGLE_API_KEY)

# 5. Create the RAG Chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | rag_prompt 
    | llm 
    | StrOutputParser()
)

# --- Define the API Endpoint ---

@router.post("/chat")
async def http_chat_with_document(request: ChatRequest):
    """
    Endpoint to ask a question about the processed document.
    """
    if retriever is None:
        raise HTTPException(status_code=500, detail="Vector store is not initialized.")

    try:
        print(f"Received question: {request.question}")
        
        # Get the answer from the RAG chain
        # .invoke() runs the chain
        answer = rag_chain.invoke(request.question)
        
        print(f"Generated answer: {answer}")
        return {"answer": answer}
        
    except Exception as e:
        print(f"Error during chat processing: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")