# Item Exchange — Part 1

Users hold item stacks. Propose an atomic swap that **reserves** inventory.

- `Exchange()`
- `set_inventory(user, item, qty)` — set that user's qty of `item` (`qty >= 0`).
- `get(user, item) -> int` — **available** qty (owned minus reserved). Missing -> `0`.
- `propose(buyer, seller, give_item, give_qty, take_item, take_qty) -> trade_id`
  Reserves `give_qty` of `give_item` from buyer and `take_qty` of `take_item` from seller.
  Insufficient available on either side -> `ValueError`.

Example:
```python
ex = Exchange()
ex.set_inventory("alice", "apple", 5)
ex.set_inventory("bob", "coin", 10)
tid = ex.propose("alice", "bob", "apple", 2, "coin", 3)
ex.get("alice", "apple")  # 3  — 2 reserved
ex.get("bob", "coin")     # 7
```
