from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/repositories",
    tags=["Chat"],
)


rag_service = RAGService()


@router.post(
    "/{repository_id}/chat",
    response_model=ChatResponse,
)
async def chat_with_repository(
    repository_id: int,
    request: ChatRequest,
):
    try:
        result = await rag_service.answer_question(
            question=request.question,
            repository_id=repository_id,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )