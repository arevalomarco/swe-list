import pytest

from solution.rate_limiter import RateLimiter


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


def test_set_limit_overrides_capacity_for_that_key_only():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)
    limiter.set_limit("vip", capacity=3)

    assert limiter.allow("vip") is True
    assert limiter.allow("vip") is True
    assert limiter.allow("vip") is True
    assert limiter.allow("vip") is False  # vip's own override, now exhausted

    assert limiter.allow("normal") is True  # unaffected, uses the base capacity of 1
    assert limiter.allow("normal") is False


def test_set_limit_rejects_non_positive_capacity():
    limiter = RateLimiter(capacity=1, window_seconds=10)
    with pytest.raises(ValueError):
        limiter.set_limit("vip", capacity=0)


def test_retry_after_reports_time_remaining_and_zero_when_available():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)

    assert limiter.retry_after() == 0.0  # nothing used yet

    limiter.allow()  # request at t=0
    assert limiter.retry_after() == pytest.approx(10.0)

    clock.advance(4)
    assert limiter.retry_after() == pytest.approx(6.0)

    clock.advance(6)  # t=10: the t=0 request has just aged out
    assert limiter.retry_after() == 0.0


def test_retry_after_does_not_itself_consume_budget():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)

    limiter.allow()
    for _ in range(5):
        limiter.retry_after()

    clock.advance(10.1)
    assert limiter.allow() is True  # still exactly one slot, not consumed by retry_after


def test_max_keys_bounds_memory_by_evicting_the_least_recently_used_key():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=100, clock=clock, max_keys=2)

    limiter.set_limit("a", capacity=5)  # configured, but never touched by allow() yet

    clock.advance(1)
    assert limiter.allow("b") is True  # b touched at t=1

    clock.advance(1)
    assert limiter.allow("c") is True  # a third key: "a" (last_used=0) is the LRU, evicted

    # "a" is gone. Re-adding it starts over with the base capacity, not the override it lost.
    assert limiter.allow("a") is True
    assert limiter.allow("a") is False


def test_unbounded_by_default_never_evicts():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=100, clock=clock)

    for i in range(50):
        clock.advance(1)
        assert limiter.allow(f"key-{i}") is True

    # Every key from earlier is still tracked with its own live budget.
    assert limiter.allow("key-0") is False
    assert limiter.allow("key-49") is False


@pytest.mark.parametrize("max_keys", [0, -1])
def test_max_keys_must_be_at_least_one_or_none(max_keys):
    with pytest.raises(ValueError):
        RateLimiter(capacity=1, window_seconds=10, max_keys=max_keys)
