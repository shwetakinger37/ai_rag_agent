import json
from typing import AsyncGenerator, List

from openai import OpenAI

from app.core.config import get_settings
from app.core.prompts import SYSTEM_PROMPT
from app.services.session_store import session_store
from app.services.vector_store import vector_store
from app.tools.calculator import calculate
from app.tools.date_time import current_datetime
from app.tools.web_search import web_search

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for recent or external information.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "current_datetime",
            "description": "Get the current date and time for a timezone.",
            "parameters": {
                "type": "object",
                "properties": {"timezone": {"type": "string", "default": "Asia/Kolkata"}},
            },
        },
    },
]


def _run_tool(name: str, arguments: dict) -> str:
    if name == "web_search":
        return web_search(arguments["query"])
    if name == "calculator":
        return calculate(arguments["expression"])
    if name == "current_datetime":
        return current_datetime(arguments.get("timezone", "Asia/Kolkata"))
    return f"Tool not found: {name}"


def _format_context(matches: List[dict]) -> str:
    if not matches:
        return "No relevant document context was found."

    context_blocks = []
    for index, match in enumerate(matches, start=1):
        metadata = match["metadata"]
        source = f"{metadata.get('filename')} | chunk {metadata.get('chunk_index')}"
        context_blocks.append(f"[Context {index}: {source}]\n{match['text']}")

    return "\n\n".join(context_blocks)


class ChatService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    def _require_api_key(self) -> None:
        if not self.settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")

    async def stream_chat(self, message: str, session_id: str, use_rag: bool = True) -> AsyncGenerator[str, None]:
        self._require_api_key()

        history = session_store.get(session_id)
        context_text = "Document retrieval was disabled for this message."

        if use_rag:
            matches = vector_store.search(message, self.settings.top_k)
            context_text = _format_context(matches)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Uploaded document context:\n{context_text}"},
            *history,
            {"role": "user", "content": message},
        ]

        tool_check = self.client.chat.completions.create(
            model=self.settings.chat_model,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )
        assistant_message = tool_check.choices[0].message

        if assistant_message.tool_calls:
            messages.append(assistant_message.model_dump())
            for tool_call in assistant_message.tool_calls:
                arguments = json.loads(tool_call.function.arguments or "{}")
                result = _run_tool(tool_call.function.name, arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        stream = self.client.chat.completions.create(
            model=self.settings.chat_model,
            messages=messages,
            stream=True,
        )

        answer = ""
        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                answer += token
                yield token

        session_store.add(session_id, "user", message)
        session_store.add(session_id, "assistant", answer)


chat_service = ChatService()
