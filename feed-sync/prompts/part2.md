# Feed Sync — Part 2

Feed B may lag. Match within `skew_ms`.

```python
sync = FeedSync(skew_ms=5)
sync.on_a(10, "B", 100, 5)
sync.on_b(12, "B", 100, 5)  # pairs — abs(10-12)<=5; same qty -> no conflict
```

## Requirements

- `FeedSync(skew_ms=0)` — part 1 is skew 0
- An A update at `t` may pair with a B update at `t'` if `abs(t-t') <= skew_ms` and `(side, price)` match; then compare qty
- Unmatched updates older than skew relative to the **latest opposite** feed timestamp become discrepancies (missing on the other side)
