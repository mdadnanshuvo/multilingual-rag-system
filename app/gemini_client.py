import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ Load .env file

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Or hardcode if needed

model = genai.GenerativeModel("models/gemini-2.0-flash")  # ✅ correct full model name

def generate_answer_with_gemini(question, contexts):
    context_text = "\n".join(contexts)
    prompt = (
        f"You are a helpful assistant.\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {question}\n\n"
        f"Answer in Bangla if the question or context is in Bangla. Otherwise, answer in English."
        f"Always mention name to indicate person or place"
    )
    response = model.generate_content(prompt)
    return response.text
