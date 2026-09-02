# BBO / NBBO — Part 2

Size at the best price.

- `get_exchange_bbo_size(exchange_id) -> (bid_size, ask_size)` — sum of `qty` at that exchange's own best bid / ask. `0` if empty on that side.
- `get_nbbo_size() -> (bid_size, ask_size)` — sum of `qty` across every exchange whose own best equals the NBBO price on that side.
- Tied NBBO prices: all tying exchanges contribute.

Example:
```python
book.add("NYSE", "o1", 100, 10, "bid")
book.add("NYSE", "o2", 100, 4, "bid")
book.add("NYSE", "o3", 99, 999, "bid")
book.get_exchange_bbo_size("NYSE")  # (14, 0)
book.add("NASDAQ", "o4", 100, 6, "bid")
book.get_nbbo_size()                # (20, 0)
```
