# LRU Cache — Part 2

Some entries must not be evicted.

- `pin(key)` / `unpin(key)`
- `pin` / `unpin` on a key not in the cache throw `std::invalid_argument`.
- A `put` that would insert a new key while every entry is pinned throws `std::invalid_argument`.
