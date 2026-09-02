# LRU Cache — Part 3

Make eviction pluggable. Pinned keys stay outside the policy.

- `Cache(capacity, policy=None)`. `policy=None` defaults to LRU among **evictable** keys.
- `LRUPolicy` and `LFUPolicy` pick the next evictable victim.
  LFU ties break by LRU among the tied keys.
- `set_policy(new_policy)` on a populated cache.
  Re-seed from the old policy's eviction order — most evictable first, **evictable keys
  only**. The very next eviction must remove the same key the old policy would have.
- `pin` removes a key from policy tracking. `unpin` puts it back (as a fresh use under
  the current policy).
- `LRUCache` from parts 1–2 keeps working from the outside (e.g. thin wrapper on `Cache`).

```python
cache = Cache(2, policy=LRUPolicy())
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.set_policy(LFUPolicy())
cache.put("c", 3)  # still evicts "b" — next victim unchanged by the swap itself
```
