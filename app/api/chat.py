from fastapi import APIRouter
from app.services.chatbot import query_chatbot

router = APIRouter()

@router.post("/ask")
def ask_question(question: str):
    """
    Processes a user's question and returns a JSON response with both the question and its AI-generated answer.
    
    The function calls the chatbot service to generate an answer for the provided question and returns a dictionary containing the original question under the key "question" and the generated answer under the key "answer".
    """
    return {"question": question, "answer": query_chatbot(question)}
