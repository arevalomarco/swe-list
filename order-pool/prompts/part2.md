# Order Pool — Part 2

Detect bad lifecycle.

- `release` of a block this pool currently considers free raises `ValueError` (double-free).
- `release` of an object this pool never returned from `allocate` raises `ValueError`.
- After a successful `release`, a later `allocate` may return that same object identity.
- Live allocations remain distinct.

Example:
```python
pool = OrderPool(8, 2)
a = pool.allocate()
pool.release(a)
pool.release(a)         # ValueError
pool.release(object())  # ValueError
```
