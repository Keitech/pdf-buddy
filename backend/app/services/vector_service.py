import chromadb

from app.services.embedding_service import create_embedding

client = chromadb.PersistentClient(path="app/chroma")

collection = client.get_or_create_collection(
    name="documents"
)


def add_chunks(document_id: str, chunks: list[str]) -> None:
    """
    Generates embeddings for document chunks and stores them in ChromaDB.
    """
    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)

        collection.add(
            ids=[f"{document_id}_{index}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "document_id": document_id,
                    "chunk": index,
                }
            ],
        )


def search_similar_chunks(question: str, n_results: int = 5):
    """
    Searches the vector database for the most relevant document chunks.
    """
    if collection.count() == 0:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    embedding = create_embedding(question)
    k = min(n_results, collection.count())

    return collection.query(
        query_embeddings=[embedding],
        n_results=k,
    )
