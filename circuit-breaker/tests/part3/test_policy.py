import pytest
from solution.circuit_breaker import (
    CircuitBreaker,
    CircuitOpenError,
    ConsecutiveFailures,
    ErrorRatePolicy,
)


class FakeClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t
    def advance(self, dt):
        self.t += dt


def test_error_rate_policy():
    clock = FakeClock()
    cb = CircuitBreaker(99, 10, clock=clock, policy=ErrorRatePolicy(window=10, rate=0.6))

    def boom():
        raise RuntimeError("x")

    assert cb.call(lambda: 1) == 1
    clock.advance(1)
    with pytest.raises(RuntimeError):
        cb.call(boom)
    # 1/2 = 0.5 < 0.6 — still closed
    clock.advance(1)
    with pytest.raises(RuntimeError):
        cb.call(boom)
    # 2 fail / 3 attempts ≈ 0.666 >= 0.6 -> open
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: 1)


def test_set_policy_resets():
    clock = FakeClock()
    cb = CircuitBreaker(2, 10, clock=clock)
    def boom():
        raise RuntimeError("x")
    with pytest.raises(RuntimeError):
        cb.call(boom)
    cb.set_policy(ConsecutiveFailures(2))
    # counter reset — need 2 more failures
    with pytest.raises(RuntimeError):
        cb.call(boom)
    assert cb.call(lambda: "ok") == "ok"
