# LRU Cache — Part 3

Make eviction pluggable. Pinned keys stay outside the policy.

- `Cache(capacity, policy=nullptr)`. `policy=nullptr` defaults to LRU among **evictable** keys.
  The caller owns `policy` when passing one in.
- `LRUPolicy` and `LFUPolicy`. LFU ties break by LRU among the tied keys.
- `set_policy(new_policy)` reseeds from the old policy's eviction order — most evictable first, evictable keys only.
- `LRUCache` from parts 1–2 keeps working from the outside.

```cpp
LRUPolicy lru;
Cache cache(2, &lru);
cache.set_policy(&lfu);  // next eviction unchanged by the swap itself
```
