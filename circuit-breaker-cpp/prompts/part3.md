# Circuit Breaker — Part 3

Pluggable trip policy. The caller owns `policy` when passing one in.

```cpp
ConsecutiveFailures consec(2);
ErrorRatePolicy rate(/*window=*/5, /*rate=*/0.5);
CircuitBreaker cb(2, 10, clock, &consec);
cb.set_policy(&rate);
```

## Requirements

- Default policy: consecutive failures (same as parts 1–2)
- `ErrorRatePolicy(window, rate)` — open when failures/attempts in the last `window` seconds >= `rate`
- `set_policy` swaps; counters / windows reset; if currently open, cool_down restarts from now
