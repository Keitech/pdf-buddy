from app.services.vector_service import search_similar_chunks


def retrieve_context(question: str) -> str:
    results = search_similar_chunks(question)
    documents = (results.get("documents") or [[]])[0] or []
    return "\n\n".join(documents)
