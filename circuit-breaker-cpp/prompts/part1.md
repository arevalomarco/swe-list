# Circuit Breaker — Part 1

```cpp
CircuitBreaker cb(2, 10, clock);
cb.call(ok_fn);     // returns result
cb.call(bad_fn);    // throws original; counts failure
// after threshold consecutive failures, further call throws CircuitOpenError without invoking fn
```

## Requirements

- `CircuitBreaker(failure_threshold, cool_down_seconds, clock={}, policy=nullptr)`
- `call(fn)` — `fn` is any nullary callable
- Exception from `fn` counts a failure; success resets consecutive failure count
- After `failure_threshold` consecutive failures, state is open: `call` throws `CircuitOpenError`

Implement in `solution/circuit_breaker.hpp`.
