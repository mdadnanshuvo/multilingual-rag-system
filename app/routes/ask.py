from fastapi import APIRouter
from pydantic import BaseModel

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
def ask_question(data: QuestionInput) -> dict:
    """
    Processes a user's question by retrieving relevant context from a vector store and generating an answer using Gemini.
    Args:
        data (QuestionInput): The input containing the user's question.
    Returns:
        dict: A dictionary with the original question and the generated answer.
    """
    question = data.question

    # Step 1: Query vector store
    top_chunks = vectorstore.query(question, top_k=10)
    contexts = [
        chunk if isinstance(chunk, str) else chunk.page_content for chunk in top_chunks
    ]

    # Step 2: Generate answer from Gemini
    answer = generate_answer_with_gemini(question, contexts)
    return {"question": question, "answer": answer}
