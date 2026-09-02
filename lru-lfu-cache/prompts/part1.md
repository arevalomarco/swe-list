# LRU Cache — Part 1

`LRUCache(capacity)`: fixed-size key-value cache. `capacity` is a positive integer.
Raise `ValueError` otherwise.

- `get(key)` returns the cached value, or `None` if absent. A hit counts as a use.
- `put(key, value)` inserts or updates. Updating an existing key counts as a use and
  does not by itself change how many entries are cached.
- A brand-new key that would push the cache past capacity evicts the least recently
  used entry first.

Example:
```python
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")  # 1
cache.put("c", 3)
cache.get("b")  # None
```
