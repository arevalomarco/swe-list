"""Rate Limiter — your implementation goes here."""

from typing import Callable, Optional


class RateLimiter:
    def __init__(
        self,
        capacity: int,
        window_seconds: float,
        clock: Optional[Callable[[], float]] = None,
    ) -> None:
        raise NotImplementedError

    def allow(self) -> bool:
        raise NotImplementedError
