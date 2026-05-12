from collections import defaultdict
from typing import Dict, List


class InMemorySessionStore:
    """Stores chat history per session. Replace with Redis/Postgres for production."""

    def __init__(self) -> None:
        self._history: Dict[str, List[dict]] = defaultdict(list)

    def get(self, session_id: str) -> List[dict]:
        return self._history[session_id]

    def add(self, session_id: str, role: str, content: str) -> None:
        self._history[session_id].append({"role": role, "content": content})
        self._history[session_id] = self._history[session_id][-20:]

    def clear(self, session_id: str) -> None:
        self._history.pop(session_id, None)


session_store = InMemorySessionStore()
