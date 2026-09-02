# Order Pool — Part 3

Thread-local cache in front of a central free-list.

- `OrderPool(block_size, capacity, cache_size=0)` — `cache_size` non-negative; invalid → `ValueError`.
  `cache_size == 0` is shared free-list (part 1/2 behaviour).
- `allocate(thread=T)`: pop from T's cache if non-empty, else central. Both empty → `None`.
- `release(block, thread=T)`: push onto T's cache if under `cache_size`, else spill to central.
- Double-free / unknown-block errors from part 2 still apply regardless of `thread`.

Example:
```python
pool = OrderPool(8, 2, cache_size=2)
a = pool.allocate(thread=0)
b = pool.allocate(thread=0)
pool.release(a, thread=0)
pool.allocate(thread=1)       # None — cannot see thread 0's cache
pool.allocate(thread=0) is a  # True
```
