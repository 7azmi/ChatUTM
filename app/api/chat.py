from fastapi import APIRouter
from app.services.chatbot import query_chatbot

router = APIRouter()

@router.post("/ask")
def ask_question(question: str):
    """
    Receives a user's question and returns the AI-generated answer.
    """
    return {"question": question, "answer": query_chatbot(question)}
