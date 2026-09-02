# LRU Cache — Part 1

`LRUCache(capacity)`: fixed-size string-to-int cache. `capacity` is a positive integer.
Throw `std::invalid_argument` otherwise.

- `get(key)` returns `optional<int>` — nullopt if absent. A hit counts as a use.
- `put(key, value)` inserts or updates. Updating an existing key counts as a use.
- A brand-new key that would push the cache past capacity evicts the least recently used entry first.

```cpp
LRUCache cache(2);
cache.put("a", 1);
cache.put("b", 2);
cache.get("a");  // 1
cache.put("c", 3);
cache.get("b");  // nullopt
```
