import os

from dotenv import load_dotenv
from openai import OpenAI

from app.services.vector_service import search_similar_chunks

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_question(question: str) -> str:
    results = search_similar_chunks(question)

    documents = (results.get("documents") or [[]])[0] or []

    if not documents:
        return "I don't know based on the provided documents."

    context = "\n\n".join(documents)

    prompt = f"""
You are an AI assistant answering questions from company documents.

Use only the provided context.

If the answer is not in the context, say:
"I don't know based on the provided documents."

Context:
{context}


Question:
{question}


Answer:
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text
