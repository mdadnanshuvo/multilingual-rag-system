from fastapi import APIRouter, UploadFile, File
import shutil
from app.loader import extract_text_from_pdf_ocr
from app.cleaner import clean_ocr_text
from app.chunker import chunk_text
from app.embedding_store import VectorStore
import os

router = APIRouter()


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    raw_text = extract_text_from_pdf_ocr(file_path)
    cleaned = clean_ocr_text(raw_text)
    chunks = chunk_text(cleaned)

    vectorstore = VectorStore()
    vectorstore.add_texts(chunks)
    vectorstore.save()

    return {"message": "PDF processed and vectorstore updated"}
