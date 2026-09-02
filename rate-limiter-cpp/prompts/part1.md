# Rate Limiter — Part 1

At most `capacity` events in any rolling `window_seconds` interval. Inject a clock so tests do not sleep.

```cpp
FakeClock clock;
RateLimiter lim(3, 10, [&clock] { return clock(); });
lim.allow();  // true, true, true, false
```

## Requirements

- `RateLimiter(capacity, window_seconds, clock={}, max_keys=nullopt)` — empty `clock` defaults to `steady_clock`. Throw `std::invalid_argument` if `capacity < 1` or `window_seconds <= 0`.
- `allow(key="default") -> bool` — counts this call if allowed. Part 1 only needs the default key.
- Rolling window, not fixed calendar buckets.

Implement in `solution/rate_limiter.hpp`.
