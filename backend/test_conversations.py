from app.db.database import SessionLocal
from app.db.conversations import (
    create_conversation,
    create_message,
    create_source_reference,
)


db = SessionLocal()

try:
    conversation = create_conversation(
        db=db,
        repository_id=1,
        title="SmartLogix Test Conversation",
    )

    print("Conversation created:", conversation.id)

    user_message = create_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content="Where is the machine learning model loaded?",
    )

    print("User message created:", user_message.id)

    assistant_message = create_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content="The model is loaded in app.py.",
    )

    print("Assistant message created:", assistant_message.id)

    source = create_source_reference(
        db=db,
        message_id=assistant_message.id,
        path="app.py",
        language="python",
        chunk_index=2,
        distance=1.2125,
    )

    print("Source reference created:", source.id)

finally:
    db.close()