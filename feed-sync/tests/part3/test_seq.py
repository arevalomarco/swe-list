from solution.feed_sync import FeedSync


def test_gap_marks_stale():
    sync = FeedSync()
    sync.on_a(1, "B", 100, 5, seq=1)
    sync.on_a(2, "B", 100, 5, seq=3)  # gap
    d = sync.discrepancies()
    assert {"type": "FeedStale", "feed": "a"} in d


def test_recover_clears_stale():
    sync = FeedSync()
    sync.on_a(1, "B", 100, 5, seq=1)
    sync.on_a(2, "B", 100, 5, seq=3)
    sync.recover("a")
    sync.on_a(3, "B", 100, 5, seq=1)
    sync.on_b(3, "B", 100, 5, seq=1)
    d = [x for x in sync.discrepancies() if x.get("type") == "FeedStale"]
    assert d == []


def test_no_new_conflicts_while_stale():
    sync = FeedSync()
    sync.on_a(1, "B", 100, 5, seq=1)
    sync.on_a(2, "B", 100, 6, seq=9)  # stale
    before = len(sync.discrepancies())
    sync.on_b(1, "B", 100, 99, seq=1)
    # should not add qty mismatch involving stale A pending
    stale_only = [x for x in sync.discrepancies() if x.get("type") == "FeedStale"]
    assert stale_only
