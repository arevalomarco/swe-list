# Order Book — Part 1

Limit order book. Price-time priority.

- A buy crosses the lowest resting sell with `sell_price <= buy_price`.
- A sell crosses the highest resting buy with `buy_price >= sell_price`.
- Fills happen at the resting order's price.
- Leftover quantity rests on the book.

- `limit(order_id, side, price, qty) -> list` of fills, in the order they happened.
  Each fill: `{"maker_order_id", "taker_order_id", "price", "qty"}`.
- `market(order_id, side, qty) -> list` of fills. Same matching loop, no price bound.
  Unfilled remainder is dropped, not rested. Against an empty opposite side -> `[]`.
- `best_bid()` / `best_ask()` — best resting price, or `None` if that side is empty.
- `cancel(order_id) -> bool` — `True` if a resting order was removed, `False` otherwise.
  A linear scan is fine for this part.

Example:
```python
book = OrderBook()
book.limit("s1", "SELL", 100, 5)
book.limit("s2", "SELL", 101, 5)
book.limit("b1", "BUY", 101, 7)
# -> [
#      {"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 5},
#      {"maker_order_id": "s2", "taker_order_id": "b1", "price": 101, "qty": 2},
#    ]
book.best_ask()  # 101
book.best_bid()  # None
```
