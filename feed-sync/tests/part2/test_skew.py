from solution.feed_sync import FeedSync


def test_skew_pairs():
    sync = FeedSync(skew_ms=5)
    sync.on_a(10, "B", 100, 5)
    sync.on_b(12, "B", 100, 5)
    assert sync.discrepancies() == []


def test_outside_skew_becomes_missing():
    sync = FeedSync(skew_ms=5)
    sync.on_a(10, "B", 100, 5)
    sync.on_b(20, "B", 101, 1)  # advances latest B; A is older than 20-5=15
    d = sync.discrepancies()
    assert any(x.get("qty_a") == 5 and x.get("qty_b") is None for x in d)


def test_skew_qty_mismatch():
    sync = FeedSync(skew_ms=3)
    sync.on_a(10, "B", 100, 5)
    sync.on_b(12, "B", 100, 7)
    d = sync.discrepancies()
    assert len(d) == 1
    assert d[0]["qty_a"] == 5 and d[0]["qty_b"] == 7
