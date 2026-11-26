from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    conversation_id: int | None = None


class SourceReference(BaseModel):
    path: str
    language: str
    chunk_index: int
    distance: float


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
    sources: list[SourceReference]