import re
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.core.config import get_settings
from app.models.schemas import ChatRequest, HealthResponse, UploadResponse
from app.services.chat_service import chat_service
from app.services.vector_store import vector_store
from app.utils.chunking import split_text
from app.utils.file_loader import load_text_from_file

router = APIRouter()
settings = get_settings()

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def _safe_name(filename: str) -> str:
    name = filename.strip() or "uploaded_file"
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", name)


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", app_name=settings.app_name)


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and MD files are supported.")

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid.uuid4())
    original_name = _safe_name(file.filename or "uploaded_file")
    saved_name = f"{document_id}_{original_name}"
    file_path = upload_dir / saved_name

    file_path.write_bytes(await file.read())

    text = load_text_from_file(str(file_path))
    if not text:
        raise HTTPException(status_code=400, detail="No readable text found in the uploaded file.")

    chunks = split_text(text)
    chunks_created = vector_store.add_chunks(document_id, original_name, chunks)

    return UploadResponse(
        document_id=document_id,
        filename=original_name,
        chunks_created=chunks_created,
        message="Document uploaded and indexed successfully.",
    )


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    async def token_generator():
        async for token in chat_service.stream_chat(request.message, request.session_id, request.use_rag):
            yield token

    return StreamingResponse(token_generator(), media_type="text/plain")
