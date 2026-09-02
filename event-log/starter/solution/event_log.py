"""Event Log — your implementation goes here."""

from typing import Any


class EventLog:
    def __init__(self) -> None:
        raise NotImplementedError

    def append(self, event_type: str, payload: Any) -> None:
        raise NotImplementedError

    def all(self) -> list[tuple[str, Any]]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
