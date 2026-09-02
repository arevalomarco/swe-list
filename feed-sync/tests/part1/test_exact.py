from solution.feed_sync import FeedSync


def test_qty_mismatch():
    sync = FeedSync()
    sync.on_a(1, "B", 100, 5)
    sync.on_b(1, "B", 100, 6)
    d = sync.discrepancies()
    assert len(d) == 1
    assert d[0]["qty_a"] == 5 and d[0]["qty_b"] == 6


def test_matching_qty_no_conflict():
    sync = FeedSync()
    sync.on_a(1, "B", 100, 5)
    sync.on_b(1, "B", 100, 5)
    assert sync.discrepancies() == []


def test_missing_on_b():
    sync = FeedSync()
    sync.on_a(1, "B", 100, 5)
    sync.on_b(1, "B", 101, 5)  # different price — both unmatched at same ts once we see both?
    # With skew 0: (1,B,100) only on A and (1,B,101) only on B -> two missing conflicts when opposite latest exists
    d = sync.discrepancies()
    assert len(d) == 2
    assert { (x["price"], x["qty_a"], x["qty_b"]) for x in d } == {
        (100, 5, None),
        (101, None, 5),
    }


def test_order_independent_pair():
    sync = FeedSync()
    sync.on_b(2, "S", 50, 1)
    sync.on_a(2, "S", 50, 1)
    assert sync.discrepancies() == []
