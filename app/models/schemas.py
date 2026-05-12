from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    session_id: str = Field(..., min_length=1, description="Client-generated session id")
    use_rag: bool = Field(default=True, description="Whether to retrieve uploaded document context")


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_created: int
    message: str


class HealthResponse(BaseModel):
    status: str
    app_name: str
