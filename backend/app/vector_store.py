from langchain_community.vectorstores import FAISS
from app.embeddings import BedrockEmbeddings
from app.config import DB_PATH

def create_vector_store(docs):
    embedding = BedrockEmbeddings()
    db = FAISS.from_documents(docs, embedding)
    db.save_local(DB_PATH)

def load_vector_store():
    embedding = BedrockEmbeddings()
    return FAISS.load_local(DB_PATH, embedding, allow_dangerous_deserialization=True)

