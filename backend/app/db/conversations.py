from sqlalchemy.orm import Session

from app.db.models import Conversation, Message, SourceReference


def create_conversation(
    db: Session,
    repository_id: int,
    title: str = "New Conversation",
) -> Conversation:
    conversation = Conversation(
        repository_id=repository_id,
        title=title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversation(
    db: Session,
    conversation_id: int,
) -> Conversation | None:
    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )


def get_repository_conversations(
    db: Session,
    repository_id: int,
) -> list[Conversation]:
    return (
        db.query(Conversation)
        .filter(Conversation.repository_id == repository_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


def create_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def create_source_reference(
    db: Session,
    message_id: int,
    path: str,
    language: str,
    chunk_index: int,
    distance: float,
) -> SourceReference:
    source = SourceReference(
        message_id=message_id,
        path=path,
        language=language,
        chunk_index=chunk_index,
        distance=str(distance),
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source