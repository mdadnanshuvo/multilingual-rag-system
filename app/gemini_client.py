import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash")


def generate_answer_with_gemini(question, contexts) -> str:
    """
    Generates an answer to a given question using the Gemini model, based on provided context.
    Args:
        question (str): The question to be answered.
        contexts (list[str]): A list of context strings relevant to the question.
    Returns:
        str: The generated answer from the Gemini model.
    """
    context_text = "\n".join(contexts)
    prompt = (
        "You are a highly intelligent and multilingual assistant specialized in answering questions based on provided context.\n\n"
        "Context:\n"
        f"{context_text}\n\n"
        "Question:\n"
        f"{question}\n\n"
        "Instructions:\n"
        "- Analyze the context carefully before answering.\n"
        "- If the question is in Bangla, answer in Bangla. Otherwise, respond in English.\n"
        "- Always mention specific names (people, places, or organizations) in your answer if referenced in the context.\n"
        "- Provide concise, factual responses rooted in the context only.\n\n"
        "Answer:"
    )

    response = model.generate_content(prompt)
    return response.text
