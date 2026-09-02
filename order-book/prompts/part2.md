# Order Book — Part 2

`cancel(order_id) -> True` if something was cancelled, `False` if it was not resting.

- Find a resting order without walking every level / every order at a level.
- Cancelling a middle order at a price must leave the remaining orders in the same time order.
- Cancelling a partially filled order removes only its remaining quantity.
- Cancelling the only order at the best price advances `best_bid` / `best_ask`.
- Cancel is idempotent. An `order_id` may be reused once it is no longer resting.

Example:
```python
book.limit("a", "SELL", 100, 3)
book.limit("b", "SELL", 100, 3)
book.limit("c", "SELL", 100, 3)
book.cancel("b")  # True
book.limit("taker", "BUY", 100, 6)
# -> fills a, then c
```
