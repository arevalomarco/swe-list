# Circuit Breaker — Part 3

Pluggable trip policy.

```python
cb = CircuitBreaker(2, 10, policy=ConsecutiveFailures(2), clock=fake)
cb.set_policy(ErrorRatePolicy(window=5, rate=0.5))
```

## Requirements

- Default policy: consecutive failures (same as parts 1–2)
- `ErrorRatePolicy(window, rate)` — open when failures/attempts in the last `window` seconds >= `rate` (need at least one attempt)
- `set_policy` swaps; consecutive counters / windows reset; if currently open, cool_down restarts from now
