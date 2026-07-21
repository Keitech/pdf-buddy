from app.services.embedding_service import create_embedding


text = "Employees receive 20 vacation days."

embedding = create_embedding(text)

print("Embedding length:", len(embedding))
print("First 5 values:", embedding[:5])