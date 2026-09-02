from solution.token_manager import TokenManager


def test_acquire_and_renew():
    mgr = TokenManager(5)
    f = mgr.acquire("res", "h1", 0)
    assert f == 1
    assert mgr.renew_lease("res", "h1", f, 1) is True
    assert mgr.acquire("res", "h2", 1) is None


def test_wrong_fence_rejected():
    mgr = TokenManager(5)
    f = mgr.acquire("res", "h1", 0)
    assert mgr.renew_lease("res", "h1", f + 1, 1) is False
    assert mgr.renew_lease("res", "other", f, 1) is False


def test_fence_increases_after_expiry():
    mgr = TokenManager(5)
    f1 = mgr.acquire("res", "h1", 0)
    f2 = mgr.acquire("res", "h2", 6)
    assert f2 > f1
    assert mgr.renew_lease("res", "h1", f1, 7) is False


def test_same_holder_reacquire():
    mgr = TokenManager(5)
    f1 = mgr.acquire("res", "h1", 0)
    f2 = mgr.acquire("res", "h1", 2)
    assert f1 == f2
