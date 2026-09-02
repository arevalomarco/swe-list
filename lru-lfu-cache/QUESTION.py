"""
LRU / LFU Cache, Part 1

LRUCache(capacity): fixed-size key-value cache. capacity is a positive integer.
Raise ValueError otherwise.

- get(key) returns the cached value, or None if absent. A hit counts as a use.
- put(key, value) inserts or updates. Updating an existing key counts as a use and
  does not by itself change how many entries are cached.
- A brand-new key that would push the cache past capacity evicts the least recently
  used entry first.

Example:
cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")  # 1
cache.put("c", 3)
cache.get("b")  # None

"""
class LRUCache:
    def __init__(self, capacity):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError




"""
PART 2

Some entries must not be evicted.

- pin(key) — that key cannot be chosen for eviction until unpinned.
- unpin(key)
- pin / unpin on a key not in the cache raise ValueError.
- A put that would insert a new key while every entry is pinned raises ValueError.

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
cache.pin("a")
cache.put("c", 3)
cache.get("b")  # None
cache.get("a")  # 1

"""


"""
PART 3

Make eviction pluggable. Pinned keys stay outside the policy.

- Cache(capacity, policy=None). policy=None defaults to LRU among evictable keys.
- LRUPolicy and LFUPolicy pick the next evictable victim.
  LFU ties break by LRU among the tied keys.
- set_policy(new_policy) on a populated cache.
  Re-seed from the old policy's eviction order — most evictable first, **evictable keys
  only**. The very next eviction must remove the same key the old policy would have.
- pin removes a key from policy tracking. unpin puts it back (as a fresh use under
  the current policy).
- LRUCache from parts 1–2 keeps working from the outside (e.g. thin wrapper on Cache).

cache = Cache(2, policy=LRUPolicy())
cache.put("a", 1)
cache.put("b", 2)
cache.get("a")
cache.set_policy(LFUPolicy())
cache.put("c", 3)  # still evicts "b" — next victim unchanged by the swap itself

"""
