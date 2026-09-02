# Rate Limiter — Part 2

Per-key limits. Same window and capacity for every key.

```python
lim = RateLimiter(2, 10, clock=fake)
lim.allow("a")  # True
lim.allow("a")  # True
lim.allow("a")  # False
lim.allow("b")  # True
```

## Requirements

- `allow(key="default") -> bool` — independent budget per key.
- No-arg `allow()` still works (uses `"default"`).
- Keys with no recent activity should not grow memory forever — discuss eviction (implemented in part 3).
