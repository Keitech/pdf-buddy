from app.services.vector_service import search_similar_chunks


questions = [
    "How much vacation do employees get?",
    "Can employees work from home?",
    "What benefits are available?"
]


for question in questions:

    print("\nQUESTION:")
    print(question)

    results = search_similar_chunks(question)

    print("\nRESULTS:")

    for document in results["documents"][0]:
        print("-", document)