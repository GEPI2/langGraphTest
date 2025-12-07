from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import shutil
import os
from src.backend.services.rag.store import VectorStore

router = APIRouter(prefix="/rag", tags=["rag"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize VectorStore
vector_store = VectorStore()

class DocumentResponse(BaseModel):
    filename: str
    status: str
    chunks_added: int

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks_count = vector_store.add_documents(file_path)
        return {"filename": file.filename, "status": "uploaded", "chunks_added": chunks_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_knowledge_base(query: str, n_results: int = 5):
    try:
        results = vector_store.query(query, n_results)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
