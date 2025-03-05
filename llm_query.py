from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import format_document
from dotenv import load_dotenv
import os

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

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are ChatUTM, a witty AI assistant for UTM students and staff. "
            "Provide accurate and useful information related to Universiti Teknologi Malaysia (UTM), including courses, facilities, events, and academic support. "
            "If the user greets you with 'hi', '/start', or similar, introduce yourself and explain how you can assist them. "
            "Use the following context to answer the user's question:\n\nContext:\n{context}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for chat history
        ("human", "{input}"),  # Placeholder for user input
    ]
)

# Initialize the Chat Model
llm = ChatOpenAI(
    model="gpt-4o-mini",  # Replace with the correct model name for GPT-4o Mini
    temperature=0.8,      # Higher temperature for more creativity
    top_p=0.9,            # Higher top_p for more diverse responses
    max_tokens=150        # Limit response length for brevity
)

# Format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Create the Runnable Chain with Retrieval
chain = (
    RunnablePassthrough.assign(
        context=lambda x: format_docs(vector_store.as_retriever().invoke(x["input"]))  # Retrieve and format docs
    )
    | prompt
    | llm
)

# Add Memory with RunnableWithMessageHistory
session_store = {}  # Store chat histories for different sessions

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
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
    # Append the latest user message to the chat history
    chat_history.append(("user", user_message))

    # Generate a response using the QA chain
    result = chain_with_history.invoke(
        {"input": user_message},
        config={"configurable": {"session_id": "user_session"}},  # Use a fixed session ID for simplicity
    )

    # Append the assistant's response to the chat history
    chat_history.append(("assistant", result.content))

    return result.content, chat_history