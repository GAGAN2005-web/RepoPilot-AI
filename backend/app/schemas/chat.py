from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )


class SourceReference(BaseModel):
    path: str
    language: str
    chunk_index: int
    distance:float 


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]