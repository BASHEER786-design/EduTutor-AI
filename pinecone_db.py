import os
import pinecone
import hashlib
from dotenv import load_dotenv
from ibm_ai import get_ibm_response

# Load API keys
load_dotenv()

# Pinecone API configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "edututor-index")

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

# Create index if not exists
if PINECONE_INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(name=PINECONE_INDEX_NAME, dimension=1536)

index = pinecone.Index(PINECONE_INDEX_NAME)

# Helper: Convert text to a vector-like hash (simulate embedding)
def fake_embedding(text):
    return [float(int(hashlib.md5((text + str(i)).encode()).hexdigest(), 16) % 1000) for i in range(1536)]

# Store a message and its response
def store_message(question, answer):
    vector = fake_embedding(question)
    index.upsert([
        ("msg-" + hashlib.md5(question.encode()).hexdigest(), vector, {"question": question, "answer": answer})
    ])

# Search similar messages
def search_memory(query, top_k=3):
    query_vector =_
