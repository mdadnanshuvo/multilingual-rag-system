import os
import shutil

from fastapi import APIRouter, File, UploadFile

from app.chunker import chunk_text
from app.cleaner import clean_ocr_text
from app.embedding_store import VectorStore
from app.loader import extract_text_from_pdf_ocr

router = APIRouter()


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)) -> dict:
    """
    Handles PDF file upload, processes the file with OCR, cleans and chunks the extracted text,
    adds the chunks to a vector store, and saves the updated vector store.
    Args:
        file (UploadFile): The uploaded PDF file.
    Returns:
        dict: A message indicating successful processing and vectorstore update.
    """
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
