# Rate Limiter — Part 3

Per-key capacity overrides and bounded memory.

```cpp
RateLimiter lim(1, 10, clock, /*max_keys=*/2);
lim.set_limit("vip", 5);
lim.retry_after("vip");  // seconds until next allow, 0 if allow would succeed
```

## Requirements

- `max_keys=nullopt` — bound distinct keys with state; `nullopt` unbounded. Throw if `max_keys < 1`.
- `set_limit(key, capacity)` — override capacity for `key`. Throw if `capacity < 1`.
- New key past `max_keys` evicts least-recently-`allow()`ed key (override + history gone). Configuring via `set_limit` does not count as a use.
- `retry_after(key="default")` — seconds until next allow; `0.0` if allow would succeed now. Does not count as a request.
