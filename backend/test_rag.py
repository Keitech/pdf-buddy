from app.services.rag_service import ask_question


answer = ask_question(
    "Where is the big banana"
)


print(answer)