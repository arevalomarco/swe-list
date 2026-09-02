"""
Circuit Breaker, Part 1

cb = CircuitBreaker(failure_threshold=2, cool_down_seconds=10, clock=fake)
cb.call(ok_fn)     # returns result
cb.call(bad_fn)    # raises original; counts failure
# after threshold consecutive failures, further call raises CircuitOpenError without invoking fn

- CircuitBreaker(failure_threshold, cool_down_seconds, clock=None)
- call(fn, args, *kwargs) -> result
- Exception from fn counts a failure; success resets consecutive failure count
- After failure_threshold consecutive failures, state is open: call raises CircuitOpenError

"""
class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold, cool_down_seconds, clock=None, policy=None):
        raise NotImplementedError

    def call(self, fn, *args, **kwargs):
        raise NotImplementedError

    def set_policy(self, policy):
        raise NotImplementedError




"""
PART 2

Half-open after cool_down.

- Once open, after cool_down_seconds a single trial call is allowed (half-open)
- Success -> closed. Failure -> open again and reset cool_down timer

"""


"""
PART 3

Pluggable trip policy.

cb = CircuitBreaker(2, 10, policy=ConsecutiveFailures(2), clock=fake)
cb.set_policy(ErrorRatePolicy(window=5, rate=0.5))

- Default policy: consecutive failures (same as parts 1–2)
- ErrorRatePolicy(window, rate) — open when failures/attempts in the last window seconds >= rate (need at least one attempt)
- set_policy swaps; consecutive counters / windows reset; if currently open, cool_down restarts from now

"""
