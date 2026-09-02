# Circuit Breaker — Part 1

```python
cb = CircuitBreaker(failure_threshold=2, cool_down_seconds=10, clock=fake)
cb.call(ok_fn)     # returns result
cb.call(bad_fn)    # raises original; counts failure
# after threshold consecutive failures, further call raises CircuitOpenError without invoking fn
```

## Requirements

- `CircuitBreaker(failure_threshold, cool_down_seconds, clock=None)`
- `call(fn, *args, **kwargs) -> result`
- Exception from `fn` counts a failure; success resets consecutive failure count
- After `failure_threshold` consecutive failures, state is open: `call` raises `CircuitOpenError`

Implement in `solution/circuit_breaker.py`.
