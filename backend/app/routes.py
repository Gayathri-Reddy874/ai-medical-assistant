from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.document_loader import load_pdf
from app.vector_store import create_vector_store
from app.rag_pipeline import get_answer
from app.config import DATA_PATH

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_pdf(file_path)
    create_vector_store(docs)

    return {"message": "File uploaded and indexed successfully"}

@router.post("/ask")
async def ask_question(query: str):
    answer, docs = get_answer(query)

    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs]
    }