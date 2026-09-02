# Feed Sync — Part 3

Sequence numbers and gaps.

```python
sync.on_a(ts, side, price, qty, seq=1)
# per feed, seq must be strictly increasing by 1; a gap marks that feed stale
sync.recover("a")  # after snapshot; clears stale
```

## Requirements

- `on_a` / `on_b` take optional `seq` (required once you start using seqs — if provided, enforce)
- Gap -> that feed becomes stale
- While a feed is stale, `discrepancies()` includes `{"type": "FeedStale", "feed": "a"|"b"}` and does not add new book conflicts involving that feed
- `recover(feed)` clears stale for that feed and resets its expected seq
