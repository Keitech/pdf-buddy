from openai import OpenAI

from app.services.vector_service import search_similar_chunks


client = OpenAI()


def ask_question(question: str) -> str:

    # 1. Retrieve relevant chunks
    results = search_similar_chunks(question)


    # 2. Build context
    documents = results["documents"][0]

    context = "\n\n".join(documents)


    # 3. Build prompt
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


    # 4. Send to LLM
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )


    # 5. Return answer
    return response.output_text