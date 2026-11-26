from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Repository
from app.db.conversations import (
    create_conversation,
    get_conversation,
    create_message,
    create_source_reference,
)
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.agent_service import AgentService


router = APIRouter()


@router.post(
    "/repositories/{repository_id}/chat",
    response_model=ChatResponse,
)
async def chat(
    repository_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    repository = (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )

    if not repository:
        raise HTTPException(
            status_code=404,
            detail="Repository not found.",
        )

    if request.conversation_id:
        conversation = get_conversation(
            db,
            request.conversation_id,
        )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

        if conversation.repository_id != repository_id:
            raise HTTPException(
                status_code=400,
                detail="Conversation does not belong to this repository.",
            )

    else:
        conversation = create_conversation(
            db,
            repository_id=repository_id,
            title=request.question[:100],
        )

    create_message(
        db,
        conversation_id=conversation.id,
        role="user",
        content=request.question,
    )

    agent_service = AgentService()

    result = await agent_service.run(
        question=request.question,
        repository_id=repository.id,
        owner=repository.owner,
        repository=repository.name,
        branch=repository.default_branch,
    )

    assistant_message = create_message(
        db,
        conversation_id=conversation.id,
        role="assistant",
        content=result["answer"],
    )

    sources = []

    if result["tool"] == "search_repository":
        for item in result["tool_result"].get("results", []):
            source = create_source_reference(
                db,
                message_id=assistant_message.id,
                path=item.get("path"),
                language=item.get("language"),
                chunk_index=item.get("chunk_index"),
                distance=item.get("distance"),
            )

            sources.append(
                {
                    "path": source.path,
                    "language": source.language,
                    "chunk_index": source.chunk_index,
                    "distance": float(source.distance),
                }
            )

    elif result["tool"] == "get_file":
        item = result["tool_result"]

        source = create_source_reference(
            db,
            message_id=assistant_message.id,
            path=item.get("path"),
            language="unknown",
            chunk_index=0,
            distance=0.0,
        )

        sources.append(
            {
                "path": source.path,
                "language": source.language,
                "chunk_index": source.chunk_index,
                "distance": float(source.distance),
            }
        )

    return ChatResponse(
        conversation_id=conversation.id,
        answer=result["answer"],
        sources=sources,
    )