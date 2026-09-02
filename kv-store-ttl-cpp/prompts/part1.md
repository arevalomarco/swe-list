# KV Store + TTL — Part 1

```cpp
KVStore kv;
kv.put("a", 1);
kv.get("a");     // 1
kv.erase("a");   // true  (erase, not delete — delete is a keyword)
kv.get("a");     // nullopt
```

## Requirements

- `KVStore()`
- `put(key, value)` — values are `int`
- `get(key) -> optional<int>`
- `erase(key) -> bool`

Implement in `solution/kv_store.hpp`.
