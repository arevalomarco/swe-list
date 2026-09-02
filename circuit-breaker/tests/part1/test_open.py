import pytest
from solution.circuit_breaker import CircuitBreaker, CircuitOpenError


class FakeClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t
    def advance(self, dt):
        self.t += dt


def test_success_passes_through():
    cb = CircuitBreaker(2, 10, clock=FakeClock())
    assert cb.call(lambda: 42) == 42


def test_opens_after_threshold():
    clock = FakeClock()
    cb = CircuitBreaker(2, 10, clock=clock)

    def boom():
        raise RuntimeError("x")

    with pytest.raises(RuntimeError):
        cb.call(boom)
    with pytest.raises(RuntimeError):
        cb.call(boom)
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: 1)


def test_success_resets_consecutive():
    clock = FakeClock()
    cb = CircuitBreaker(2, 10, clock=clock)

    def boom():
        raise RuntimeError("x")

    with pytest.raises(RuntimeError):
        cb.call(boom)
    assert cb.call(lambda: "ok") == "ok"
    with pytest.raises(RuntimeError):
        cb.call(boom)
    # only 1 consecutive failure — still closed
    assert cb.call(lambda: "ok2") == "ok2"
