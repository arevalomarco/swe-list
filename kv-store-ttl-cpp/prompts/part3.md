# KV Store + TTL — Part 3

Watchers. `unwatch(key)` removes all callbacks for that key.

```cpp
kv.watch("a", cb);
kv.put("a", 2);      // cb("a", 2)
kv.erase("a");       // cb("a", nullopt)
kv.expire_due();     // notifies watchers for newly discovered expiries
```

## Requirements

- `watch(key, callback)` / `unwatch(key)`
- `callback(key, new_value_or_nullopt)` on put/erase/expiry
- Expiry must notify when discovered via `get` or `expire_due()`
