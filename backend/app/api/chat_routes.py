from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import ask_question

router = APIRouter(prefix="/chat", tags=["Chat"])


class Question(BaseModel):
    question: str


@router.post("/")
async def chat(request: Question):

    answer = ask_question(request.question)

    return {
        "answer": answer
    }