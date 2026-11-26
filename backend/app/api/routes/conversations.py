from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.conversations import (
    get_conversation,
    get_repository_conversations,
)
from app.db.database import get_db


router = APIRouter(
    tags=["Conversations"],
)


@router.get("/repositories/{repository_id}/conversations")
def list_conversations(
    repository_id: int,
    db: Session = Depends(get_db),
):
    conversations = get_repository_conversations(
        db=db,
        repository_id=repository_id,
    )

    return [
        {
            "id": conversation.id,
            "repository_id": conversation.repository_id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
        }
        for conversation in conversations
    ]


@router.get("/conversations/{conversation_id}")
def get_conversation_history(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return {
        "id": conversation.id,
        "repository_id": conversation.repository_id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
                "sources": [
                    {
                        "path": source.path,
                        "language": source.language,
                        "chunk_index": source.chunk_index,
                        "distance": float(source.distance),
                    }
                    for source in message.source_references
                ],
            }
            for message in conversation.messages
        ],
    }