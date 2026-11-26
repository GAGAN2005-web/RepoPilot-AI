from sqlalchemy import Column, Integer, String, Text

from app.db.database import Base

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    owner = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(String(500), unique=True, nullable=False)

    description = Column(Text, nullable=True)
    language = Column(String(100), nullable=True)

    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)

    default_branch = Column(String(255), nullable=False)

    indexing_status = Column(
        String(50),
        default="pending",
        nullable=False,
    )

    conversations = relationship(
    "Conversation",
    back_populates="repository",
    cascade="all, delete-orphan",
    )



# Keep your existing Repository model above this.


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)

    title = Column(String(200), nullable=False, default="New Conversation")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    repository = relationship("Repository", back_populates="conversations")
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False,
    )

    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")

    source_references = relationship(
        "SourceReference",
        back_populates="message",
        cascade="all, delete-orphan",
    )


class SourceReference(Base):
    __tablename__ = "source_references"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(
        Integer,
        ForeignKey("messages.id"),
        nullable=False,
    )

    path = Column(String(500), nullable=False)
    language = Column(String(50), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    distance = Column(String(50), nullable=False)

    message = relationship("Message", back_populates="source_references")