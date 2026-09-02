# Rate Limiter — Part 3

Per-key capacity overrides and bounded memory.

```python
lim = RateLimiter(1, 10, max_keys=2, clock=fake)
lim.set_limit("vip", 5)
lim.allow("vip")     # True (1 of 5)
lim.allow("normal")  # True (1 of 1)
lim.allow("third")   # may evict least-recently-used key (incl. override)
```

## Requirements

- `RateLimiter(..., max_keys=None)` — bound distinct keys with state; `None` unbounded. Raise `ValueError` if `max_keys < 1`.
- `set_limit(key, capacity)` — override capacity for `key`. Raise if `capacity < 1`.
- New key past `max_keys` evicts least-recently-`allow()`ed key (override + history gone).
- `retry_after(key="default") -> float` — seconds until next allow; `0.0` if allow would succeed now. Does not count as a request.
