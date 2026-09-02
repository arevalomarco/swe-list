# BBO / NBBO — Part 3

`cancel(order_id) -> bool`.

- `True` if a resting order was removed, `False` if unknown or already cancelled (idempotent).
- Cancelling the only order at an exchange's best price advances that BBO (or to `None`).
- If that exchange set the NBBO, NBBO must move to the next best venue.
- Size helpers from part 2 must stay correct after cancel.

Example:
```python
book.add("NYSE", "o1", 100, 10, "bid")
book.add("NASDAQ", "o2", 99, 5, "bid")
book.get_nbbo()  # (100, None)
book.cancel("o1")
book.get_exchange_bbo("NYSE")  # (None, None)
book.get_nbbo()                # (99, None)
```
