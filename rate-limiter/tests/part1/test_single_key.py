import pytest

from solution.rate_limiter import RateLimiter


class FakeClock:
    """A controllable clock so window behavior is tested without sleeping."""

    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


def test_allows_up_to_capacity_then_denies():
    clock = FakeClock()
    limiter = RateLimiter(capacity=3, window_seconds=10, clock=clock)

    assert limiter.allow() is True
    assert limiter.allow() is True
    assert limiter.allow() is True
    assert limiter.allow() is False


def test_capacity_frees_up_as_the_window_slides_past_old_requests():
    clock = FakeClock()
    limiter = RateLimiter(capacity=2, window_seconds=10, clock=clock)

    assert limiter.allow() is True  # request at t=0

    clock.advance(5)
    assert limiter.allow() is True  # request at t=5, both still within any 10s window

    clock.advance(5.5)  # t=10.5: the t=0 request is now more than 10s old
    assert limiter.allow() is True  # only the t=5 request still counts
    assert limiter.allow() is False  # now two requests (t=5, t=10.5) are live


def test_a_fully_elapsed_window_resets_capacity():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)

    assert limiter.allow() is True
    assert limiter.allow() is False

    clock.advance(10.1)
    assert limiter.allow() is True


def test_a_fixed_reset_boundary_would_wrongly_allow_double_capacity():
    # The failure mode a fixed-window counter has and a sliding window must not: capacity
    # right before a boundary, plus capacity again right after it, within less than one
    # window's worth of real time.
    clock = FakeClock()
    limiter = RateLimiter(capacity=2, window_seconds=10, clock=clock)

    assert limiter.allow() is True
    assert limiter.allow() is True

    clock.advance(9.9)  # just before a hypothetical reset at t=10
    assert limiter.allow() is False  # both earlier requests are still within the last 10s


@pytest.mark.parametrize("capacity", [0, -1])
def test_non_positive_capacity_is_rejected(capacity):
    with pytest.raises(ValueError):
        RateLimiter(capacity=capacity, window_seconds=10)


@pytest.mark.parametrize("window_seconds", [0, -5])
def test_non_positive_window_is_rejected(window_seconds):
    with pytest.raises(ValueError):
        RateLimiter(capacity=1, window_seconds=window_seconds)
