from typing import List

import chromadb
from openai import OpenAI

from app.core.config import get_settings


class VectorStoreService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = chromadb.PersistentClient(path=self.settings.chroma_dir)
        self.collection = self.client.get_or_create_collection(name="documents")
        self.openai_client = OpenAI(api_key=self.settings.openai_api_key)

    def _require_api_key(self) -> None:
        if not self.settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")

    def _embed(self, texts: List[str]) -> List[List[float]]:
        self._require_api_key()
        response = self.openai_client.embeddings.create(
            model=self.settings.embedding_model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def add_chunks(self, document_id: str, filename: str, chunks: List[str]) -> int:
        if not chunks:
            return 0

        embeddings = self._embed(chunks)
        chunk_ids = [f"{document_id}_{index}" for index in range(len(chunks))]
        metadata = [
            {"document_id": document_id, "filename": filename, "chunk_index": index}
            for index in range(len(chunks))
        ]

        self.collection.add(ids=chunk_ids, documents=chunks, embeddings=embeddings, metadatas=metadata)
        return len(chunks)

    def search(self, query: str, top_k: int | None = None) -> List[dict]:
        result_count = top_k or self.settings.top_k
        query_embedding = self._embed([query])[0]
        result = self.collection.query(query_embeddings=[query_embedding], n_results=result_count)

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
            {"text": document, "metadata": metadata, "distance": distance}
            for document, metadata, distance in zip(documents, metadatas, distances)
        ]


vector_store = VectorStoreService()
