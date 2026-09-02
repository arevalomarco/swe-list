import pytest
from solution.circuit_breaker import CircuitBreaker, CircuitOpenError


class FakeClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t
    def advance(self, dt):
        self.t += dt


def open_breaker(cb, clock, n=2):
    def boom():
        raise RuntimeError("x")
    for _ in range(n):
        with pytest.raises(RuntimeError):
            cb.call(boom)


def test_half_open_success_closes():
    clock = FakeClock()
    cb = CircuitBreaker(2, 10, clock=clock)
    open_breaker(cb, clock)
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: 1)
    clock.advance(10)
    assert cb.call(lambda: "ok") == "ok"
    assert cb.call(lambda: "still") == "still"


def test_half_open_failure_reopens():
    clock = FakeClock()
    cb = CircuitBreaker(2, 10, clock=clock)
    open_breaker(cb, clock)
    clock.advance(10)

    def boom():
        raise RuntimeError("x")

    with pytest.raises(RuntimeError):
        cb.call(boom)
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: 1)
    clock.advance(9.9)
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: 1)
