# Import the main FastAPI class
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our new API routers
from app.api.routes import upload
from app.api.routes import chat
from app.api.routes import reset

# Create an "instance" of the FastAPI class
# This 'app' variable is the main entry point for our entire backend
app = FastAPI(
    title="Document Intelligence API",
    description="API for the AI-Powered Document Intelligence System",
    version="0.1.0",
)

# --- CORS Middleware ---
# (Cross-Origin Resource Sharing)
# This is crucial for allowing our Next.js frontend
# (running on http://localhost:3000)
# to talk to our backend (running on http://localhost:8000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Only allow our frontend
    # You can restrict this to ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- Include API Routers ---
# This tells the main 'app' to include all the routes
# defined in the 'upload' and 'chat' routers.
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(reset.router, prefix="/api", tags=["Reset"])



# Define our first "endpoint" or "route"
# A "decorator" that tells FastAPI what to do
# --- Root Endpoint ---
@app.get("/")
def get_root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "API is running. Go to /docs for interactive documentation."}