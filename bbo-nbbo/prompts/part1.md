# BBO / NBBO — Part 1

Resting quotes across exchanges. No matching — orders just rest.

- `add(exchange_id, order_id, price, qty, side)` — `side` in `{"bid","ask"}`.
- `get_exchange_bbo(exchange_id) -> (best_bid, best_ask)`. `None` per empty side. Unknown exchange → `(None, None)`.
- `get_nbbo() -> (max bid, min ask)` across exchanges.

Example:
```python
book = MultiExchangeBook()
book.add("NYSE", "o1", 100, 10, "bid")
book.add("NYSE", "o2", 105, 5, "ask")
book.get_exchange_bbo("NYSE")  # (100, 105)
book.add("NASDAQ", "o3", 101, 1, "bid")
book.get_nbbo()                # (101, 105)
```
