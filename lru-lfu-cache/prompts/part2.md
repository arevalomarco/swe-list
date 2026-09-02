# LRU Cache — Part 2

Some entries must not be evicted.

- `pin(key)` — that key cannot be chosen for eviction until unpinned.
- `unpin(key)`
- `pin` / `unpin` on a key not in the cache raise `ValueError`.
- A `put` that would insert a new key while every entry is pinned raises `ValueError`.

```python
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.pin("a")
cache.put("c", 3)
cache.get("b")  # None
cache.get("a")  # 1
```
