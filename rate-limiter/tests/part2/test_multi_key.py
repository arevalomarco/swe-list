from solution.rate_limiter import RateLimiter


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


def test_allow_with_no_key_behaves_like_part_1():
    clock = FakeClock()
    limiter = RateLimiter(capacity=2, window_seconds=10, clock=clock)

    assert limiter.allow() is True
    assert limiter.allow() is True
    assert limiter.allow() is False


def test_different_keys_have_fully_independent_budgets():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)

    assert limiter.allow("alice") is True
    assert limiter.allow("bob") is True  # bob's budget is untouched by alice's usage
    assert limiter.allow("alice") is False
    assert limiter.allow("bob") is False


def test_the_same_key_shares_its_budget_across_calls():
    clock = FakeClock()
    limiter = RateLimiter(capacity=2, window_seconds=10, clock=clock)

    assert limiter.allow("x") is True
    assert limiter.allow("x") is True
    assert limiter.allow("x") is False


def test_a_never_before_seen_key_starts_with_a_full_budget():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)

    limiter.allow("a")  # exhausts "a"
    assert limiter.allow("z") is True  # "z" is unrelated and unaffected


def test_each_key_slides_its_own_window_independently():
    clock = FakeClock()
    limiter = RateLimiter(capacity=1, window_seconds=10, clock=clock)

    assert limiter.allow("a") is True
    clock.advance(5)
    assert limiter.allow("b") is True
    clock.advance(5.1)  # "a"'s request (t=0) has aged out; "b"'s (t=5) has not
    assert limiter.allow("a") is True
    assert limiter.allow("b") is False
