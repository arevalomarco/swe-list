# Order Pool — Part 1

Fixed-capacity pool of fixed-size blocks. No malloc on allocate after construction.

- `OrderPool(block_size, capacity)` — both positive integers; raise `ValueError` otherwise.
- `allocate(thread=0)` — mutable bytes-like of length `block_size`, or `None` if exhausted. `thread` unused here.
- `release(block, thread=0)` — return block to the pool. `thread` unused here.
- At most `capacity` live at once. Live allocations are distinct objects.

Example:
```python
pool = OrderPool(block_size=8, capacity=2)
a = pool.allocate()
b = pool.allocate()
pool.allocate()  # None
pool.release(a)
pool.allocate()  # reuses a slot
```
