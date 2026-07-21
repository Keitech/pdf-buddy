from openai import OpenAI

from app.services.retrieval_service import retrieve_context

client = OpenAI()


def ask_question(question: str):

    context = retrieve_context(question)

    prompt = f"""
You are an AI assistant.

Use ONLY the context below.

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text