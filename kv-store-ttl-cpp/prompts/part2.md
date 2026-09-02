# KV Store + TTL — Part 2

```cpp
KVStore kv(clock);
kv.put("a", 1, /*ttl=*/10);
// after 10s...
kv.get("a");  // nullopt — entry dropped lazily
```

## Requirements

- `KVStore(clock={})` — empty clock defaults to 0 (tests inject one)
- `put(key, value, ttl=nullopt)` — `ttl` seconds from now; `nullopt` means forever
- `get` on expired key returns nullopt and drops the entry
- `put` without `ttl` on an existing key clears ttl
