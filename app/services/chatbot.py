import os
import faiss
from dotenv import load_dotenv
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

load_dotenv()

# Load OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Sample university data
university_data = """
[University Information]
Name: University of Example
Founded: 1950
Location: Example City

[Departments]
- Computer Science: AI, ML, Networking
- Engineering: Electrical, Mechanical, Civil
- Business: Finance, Marketing, Management

[Admissions]
Requirements: GPA 3.0+, SAT/ACT, Personal Statement
Deadline: March 31st

[Contact]
Email: admissions@example.edu
Phone: +123456789
"""

# Convert sample data into LangChain documents
documents = [Document(page_content=university_data)]

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Create FAISS vector store
db = FAISS.from_documents(texts, embeddings)

# Save and load FAISS index
db.save_local("faiss_index")
db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Initialize ChatGPT as LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# Create LangChain RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())

def query_chatbot(question: str) -> str:
    """
    Handles chatbot queries by retrieving the best-matching answer from FAISS.
    """
    response = qa_chain.invoke(question)
    return response
