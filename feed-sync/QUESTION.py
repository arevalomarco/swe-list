"""
Feed Sync, Part 1

Two feeds A and B emit (timestamp, side, price, qty) for one instrument.

sync = FeedSync()
sync.on_a(1, "B", 100, 5)
sync.on_b(1, "B", 100, 6)
sync.discrepancies()  # one conflict: qty differs at same ts/side/price

- FeedSync() / on_a(...) / on_b(...)
- discrepancies() -> list of conflicts seen so far
- A conflict is same (ts, side, price) where qty differs, or a level present on one feed at ts and missing on the other at the same ts
- Conflict shape: {"ts", "side", "price", "qty_a", "qty_b"} with missing side as None

"""
class FeedSync:
    def __init__(self, skew_ms=0):
        raise NotImplementedError

    def on_a(self, ts, side, price, qty, seq=None):
        raise NotImplementedError

    def on_b(self, ts, side, price, qty, seq=None):
        raise NotImplementedError

    def discrepancies(self):
        raise NotImplementedError

    def recover(self, feed):
        raise NotImplementedError




"""
PART 2

Feed B may lag. Match within skew_ms.

sync = FeedSync(skew_ms=5)
sync.on_a(10, "B", 100, 5)
sync.on_b(12, "B", 100, 5)  # pairs — abs(10-12)<=5; same qty -> no conflict

- FeedSync(skew_ms=0) — part 1 is skew 0
- An A update at t may pair with a B update at t' if abs(t-t') <= skew_ms and (side, price) match; then compare qty
- Unmatched updates older than skew relative to the latest opposite feed timestamp become discrepancies (missing on the other side)

"""


"""
PART 3

Sequence numbers and gaps.

sync.on_a(ts, side, price, qty, seq=1)
# per feed, seq must be strictly increasing by 1; a gap marks that feed stale
sync.recover("a")  # after snapshot; clears stale

- on_a / on_b take optional seq (required once you start using seqs — if provided, enforce)
- Gap -> that feed becomes stale
- While a feed is stale, discrepancies() includes {"type": "FeedStale", "feed": "a"|"b"} and does not add new book conflicts involving that feed
- recover(feed) clears stale for that feed and resets its expected seq

"""
