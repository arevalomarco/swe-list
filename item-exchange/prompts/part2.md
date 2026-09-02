# Item Exchange — Part 2

Settle or drop a proposal.

- `accept(trade_id)` — move reserved balances:
  buyer loses `give`, gains `take`; seller loses `take`, gains `give`.
- `cancel(trade_id)` — release reservations; inventories unchanged aside from frees.
- Accept or cancel twice (or on unknown / already settled id) -> `ValueError`.
- After accept/cancel, reserved qty is gone from that trade.

```python
ex.accept(tid)
ex.get("alice", "apple")  # 3
ex.get("alice", "coin")   # 3
ex.get("bob", "apple")    # 2
ex.get("bob", "coin")     # 7
ex.accept(tid)            # ValueError
```
