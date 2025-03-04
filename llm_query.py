from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA


# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize embeddings and vector store
embeddings = OpenAIEmbeddings()
vector_store = Chroma(
    persist_directory="./data/chroma_data",
    embedding_function=embeddings
)

# Initialize the conversational retrieval chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=OpenAI(),
    retriever=vector_store.as_retriever()
)

def get_response(user_message, chat_history):
    """
    Generate a response from the LLM based on user input and chat history.

    Args:
        user_message (str): The latest message from the user.
        chat_history (list): List of tuples containing past interactions.

    Returns:
        tuple: A tuple containing the response string and the updated chat history.
    """
    # Define an instruction for ChatUTM
    instruction = (
        "You are ChatUTM, an AI assistant designed to help UTM students and staff. "
        "Provide accurate and useful information related to Universiti Teknologi Malaysia (UTM), including courses, facilities, events, and academic support. "
        "If the user greets you with 'hi', '/start', or similar, introduce yourself and explain how you can assist them."
    )

    # Handle generic messages
    if user_message.lower() in ["hi", "/start", "hello"]:
        return (
            "Hello! I'm ChatUTM, an AI assistant for UTM students and staff. "
            "I can help with university-related queries, including courses, facilities, events, and more. "
            "How can I assist you today?",
            chat_history
        )

    # Append the latest user message to the chat history
    chat_history.append(("user", user_message))

    # Generate a response using the QA chain
    result = qa_chain.invoke({"question": f"{instruction}\nUser: {user_message}", "chat_history": chat_history})

    # Append the assistant's response to the chat history
    chat_history.append(("assistant", result["answer"]))

    return result["answer"], chat_history

