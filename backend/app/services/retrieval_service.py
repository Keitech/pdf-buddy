from app.services.vector_store import search_similar_chunks


def retrieve_context(question: str):

    results = search_similar_chunks(question)

    documents = results["documents"][0]

    return "\n\n".join(documents)