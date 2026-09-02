# Order Book — Part 3

`amend(order_id, new_qty) -> bool`. `True` if a resting order was changed.

- Shrink keeps time priority.
- Grow re-queues at the back of that price. Same `order_id`. Does not match on the way in.
- `new_qty == 0` is cancel.
- `new_qty == current_qty` is a successful no-op (`True`).
- Negative `new_qty` raises `ValueError`.
- Amend never changes price, so it can never cross.

Example:
```python
book = OrderBook()
book.limit("a", "SELL", 100, 5)
book.limit("b", "SELL", 100, 5)
book.amend("a", 2)
book.limit("t", "BUY", 100, 6)
# -> fills 2 from a, then 4 from b

book.limit("c", "SELL", 100, 5)
book.amend("c", 9)
book.limit("t2", "BUY", 100, 5)
# -> b's remaining 1 fills before c
```
