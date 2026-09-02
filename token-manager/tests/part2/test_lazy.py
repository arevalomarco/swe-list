from solution.token_manager import TokenManager


def test_many_expired_purged_from_count():
    mgr = TokenManager(1)
    for i in range(50):
        mgr.generate(f"t{i}", 0)
    assert mgr.count_unexpired(0) == 50
    assert mgr.count_unexpired(2) == 0
    mgr.generate("fresh", 2)
    assert mgr.count_unexpired(2) == 1


def test_renew_extends():
    mgr = TokenManager(5)
    mgr.generate("t", 0)
    mgr.renew("t", 4)
    assert mgr.count_unexpired(8) == 1
