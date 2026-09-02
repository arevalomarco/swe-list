# Item Exchange — Part 3

Multi-leg trades — all legs reserved or none.

- `propose_legs(legs) -> trade_id` where each leg is
  `(from_user, to_user, item, qty)`.
- Reserve every leg; if any leg lacks available qty, roll back all reservations
  and raise `ValueError`.
- `accept` / `cancel` work on multi-leg trades the same way (atomic apply / release).

```python
ex.set_inventory("a", "x", 1)
ex.set_inventory("b", "y", 1)
ex.set_inventory("c", "z", 1)
tid = ex.propose_legs([
    ("a", "b", "x", 1),
    ("b", "c", "y", 1),
    ("c", "a", "z", 1),
])
ex.accept(tid)
# a has z, b has x, c has y
```
