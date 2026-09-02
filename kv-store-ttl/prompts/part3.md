# KV Store + TTL — Part 3

Watchers.

```python
def cb(key, new_value): ...
kv.watch("a", cb)
kv.put("a", 2)       # cb("a", 2)
kv.delete("a")       # cb("a", None)
kv.expire_due(now)   # notifies watchers for newly discovered expiries
```

## Requirements

- `watch(key, callback)` / `unwatch(key, callback)`
- `callback(key, new_value_or_None)` on put/delete/expiry
- Expiry must notify when discovered via `get` or `expire_due(now)`
