# Rate Limiter — Part 1

At most `capacity` events in any rolling `window_seconds` interval. Inject a clock so tests do not sleep.

```python
lim = RateLimiter(capacity=3, window_seconds=10, clock=fake)
lim.allow()  # True
lim.allow()  # True
lim.allow()  # True
lim.allow()  # False
```

## Requirements

- `RateLimiter(capacity, window_seconds, clock=None)` — `clock` defaults to `time.monotonic`. Raise `ValueError` if `capacity < 1` or `window_seconds <= 0`.
- `allow() -> bool` — counts this call if allowed.
- Rolling window, not fixed calendar buckets (fixed reset wrongly allows `2 * capacity` across a boundary).

Implement in `solution/rate_limiter.py`.
