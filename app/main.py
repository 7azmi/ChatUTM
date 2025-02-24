from fastapi import FastAPI
from app.api import chat, user
import os

# Load environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI(title="ChatUTM API", description="AI-powered knowledge assistant for UTM.")

# Register Routes
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(user.router, prefix="/user", tags=["User"])

@app.get("/")
def root():
    """
    Return a welcome message for ChatUTM.
    
    Returns:
        dict: A dictionary with a 'message' key containing the welcome text.
    """
    return {"message": "Welcome to ChatUTM!"}
