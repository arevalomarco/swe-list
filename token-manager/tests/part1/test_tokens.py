from solution.token_manager import TokenManager


def test_pad_example():
    mgr = TokenManager(5)
    mgr.generate("t1", 1)
    mgr.renew("t1", 2)
    assert mgr.count_unexpired(6) == 1
    assert mgr.count_unexpired(8) == 0


def test_generate_and_count():
    mgr = TokenManager(10)
    mgr.generate("a", 0)
    mgr.generate("b", 0)
    assert mgr.count_unexpired(0) == 2
    assert mgr.count_unexpired(10) == 0


def test_renew_missing_is_noop():
    mgr = TokenManager(5)
    mgr.renew("nope", 1)
    assert mgr.count_unexpired(1) == 0


def test_renew_expired_is_noop():
    mgr = TokenManager(5)
    mgr.generate("t", 0)
    mgr.renew("t", 6)
    assert mgr.count_unexpired(6) == 0


def test_regenerate_resets_expiry():
    mgr = TokenManager(5)
    mgr.generate("t", 0)
    mgr.generate("t", 4)
    assert mgr.count_unexpired(8) == 1
    assert mgr.count_unexpired(10) == 0
