from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Repository
from app.schemas.chat import ChatRequest
from app.services.agent_service import AgentService


router = APIRouter()


@router.post("/repositories/{repository_id}/agent-chat")
async def agent_chat(
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

    agent_service = AgentService()

    result = await agent_service.run(
        question=request.question,
        repository_id=repository.id,
        owner=repository.owner,
        repository=repository.name,
        branch=repository.default_branch,
    )

    sources = []

    if result["tool"] == "search_repository":
        for item in result["tool_result"].get("results", []):
            sources.append(
                {
                    "path": item.get("path"),
                    "language": item.get("language"),
                    "chunk_index": item.get("chunk_index"),
                    "distance": item.get("distance"),
                }
            )

    elif result["tool"] == "get_file":
        sources.append(
            {
                "path": result["tool_result"].get("path"),
                "language": "unknown",
                "chunk_index": 0,
                "distance": 0.0,
            }
        )

    return {
        "repository_id": repository.id,
        "question": request.question,
        "answer": result["answer"],
        "tool_used": result["tool"],
        "sources": sources,
    }