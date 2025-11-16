from pydantic import BaseModel

# BaseModel is from Pydantic
class ChatRequest(BaseModel):
    """
    Defines the shape of a request to the /chat endpoint.
    """
    question: str
    # We could add more fields here later, like 'conversation_id'