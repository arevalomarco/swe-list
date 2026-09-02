# Feed Sync — Part 1

Two feeds A and B emit `(timestamp, side, price, qty)` for one instrument.

```python
sync = FeedSync()
sync.on_a(1, "B", 100, 5)
sync.on_b(1, "B", 100, 6)
sync.discrepancies()  # one conflict: qty differs at same ts/side/price
```

## Requirements

- `FeedSync()` / `on_a(...)` / `on_b(...)`
- `discrepancies() -> list` of conflicts seen so far
- A conflict is same `(ts, side, price)` where qty differs, **or** a level present on one feed at `ts` and missing on the other at the same `ts`
- Conflict shape: `{"ts", "side", "price", "qty_a", "qty_b"}` with missing side as `None`

Implement in `solution/feed_sync.py`.
