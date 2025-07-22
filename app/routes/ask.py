from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.loader import extract_text_from_pdf_ocr
from app.cleaner import clean_ocr_text
from app.chunker import chunk_text
from app.embedding_store import VectorStore
from app.gemini_client import generate_answer_with_gemini


router = APIRouter()

# Optional: Only load vector store once
vectorstore = VectorStore()
vectorstore.load()


# Define input model
class QuestionInput(BaseModel):
    question: str

@router.post("/")
def ask_question(data: QuestionInput):
    question = data.question

    # Step 1: Query vector store
    top_chunks = vectorstore.query(question, top_k=3)
    contexts = [chunk if isinstance(chunk, str) else chunk.page_content for chunk in top_chunks]

    # Step 2: Generate answer from Gemini
    answer = generate_answer_with_gemini(question, contexts)
    return {"question": question, "answer": answer}
