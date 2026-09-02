"""
Rate Limiter, Part 1

At most capacity events in any rolling window_seconds interval. Inject a clock so tests do not sleep.

lim = RateLimiter(capacity=3, window_seconds=10, clock=fake)
lim.allow()  # True
lim.allow()  # True
lim.allow()  # True
lim.allow()  # False

- RateLimiter(capacity, window_seconds, clock=None) — clock defaults to time.monotonic. Raise ValueError if capacity < 1 or window_seconds <= 0.
- allow() -> bool — counts this call if allowed.
- Rolling window, not fixed calendar buckets (fixed reset wrongly allows 2 * capacity across a boundary).

"""
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




"""
PART 2

Per-key limits. Same window and capacity for every key.

lim = RateLimiter(2, 10, clock=fake)
lim.allow("a")  # True
lim.allow("a")  # True
lim.allow("a")  # False
lim.allow("b")  # True

- allow(key="default") -> bool — independent budget per key.
- No-arg allow() still works (uses "default").
- Keys with no recent activity should not grow memory forever — discuss eviction (implemented in part 3).

"""


"""
PART 3

Per-key capacity overrides and bounded memory.

lim = RateLimiter(1, 10, max_keys=2, clock=fake)
lim.set_limit("vip", 5)
lim.allow("vip")     # True (1 of 5)
lim.allow("normal")  # True (1 of 1)
lim.allow("third")   # may evict least-recently-used key (incl. override)

- RateLimiter(..., max_keys=None) — bound distinct keys with state; None unbounded. Raise ValueError if max_keys < 1.
- set_limit(key, capacity) — override capacity for key. Raise if capacity < 1.
- New key past max_keys evicts least-recently-allow()ed key (override + history gone).
- retry_after(key="default") -> float — seconds until next allow; 0.0 if allow would succeed now. Does not count as a request.

"""
