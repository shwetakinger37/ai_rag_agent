from fastapi import FastAPI
from app.api.routes import router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "AI RAG Agent Chatbot is running. Visit /docs for API docs."}
