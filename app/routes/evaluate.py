from fastapi import APIRouter
from sentence_transformers import SentenceTransformer, util

from app.embedding_store import VectorStore
from app.gemini_client import generate_answer_with_gemini
from app.translator import detect_language, translate_to_bangla

router = APIRouter()

model = SentenceTransformer("all-MiniLM-L6-v2")

EVALUATION_SET = [
    {
        "question": "কাকে অনুপমের ভাগ্য দেবতা বলা হয়েছে?",
        "expected_keywords": ["অনুপম", "ভাগ্য", "দেবতা", "মামা"],
    },
    {
        "question": "Who is referred to as Anupam's god of fortune?",
        "expected_keywords": ["Anupam", "fortune", "god", "uncle", "mama"],
    },
    {
        "question": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
        "expected_keywords": ["অনুপম", "সুপুরুষ", "শম্ভুনাথ"],
    },
    {
        "question": "According to Anupam, who is described as a noble man?",
        "expected_keywords": ["Anupam", "noble", "man", "Shambhunath"],
    },
]


@router.get("/")
def run_evaluation() -> dict:
    """
    Runs evaluation on a predefined set of questions by generating answers,
    scoring keyword matches, and calculating groundedness via cosine similarity.
    Returns:
        dict: A dictionary containing the evaluation status, total number of evaluated items,
        and a list of results with question, answer, expected keywords, keyword score, and groundedness score.
    """
    vectorstore = VectorStore()
    vectorstore.load()

    results = []

    for item in EVALUATION_SET:
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        # Translate if necessary
        lang = detect_language(question)
        translated_question = (
            translate_to_bangla(question) if lang == "en" else question
        )

        top_chunks = vectorstore.query(translated_question, top_k=3)
        contexts = [
            chunk if isinstance(chunk, str) else chunk.page_content
            for chunk in top_chunks
        ]

        answer = generate_answer_with_gemini(
            question, contexts
        )  # original question retained for final answer
        hits = sum(1 for kw in expected_keywords if kw.lower() in answer.lower())
        keyword_score = hits / len(expected_keywords)

        # Groundedness via cosine similarity
        answer_embedding = model.encode(answer, convert_to_tensor=True)
        context_embeddings = model.encode(contexts, convert_to_tensor=True)
        cosine_scores = util.cos_sim(answer_embedding, context_embeddings)
        groundedness_score = float(cosine_scores.max())

        results.append(
            {
                "question": question,
                "answer": answer,
                "expected_keywords": expected_keywords,
                "score": round(keyword_score, 2),
                "groundedness_score": round(groundedness_score, 2),
            }
        )

    return {"status": "completed", "total": len(results), "results": results}
