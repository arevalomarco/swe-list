# KV Store + TTL — Part 2

```python
kv = KVStore(clock=fake)
kv.put("a", 1, ttl=10)
# after 10s...
kv.get("a")  # None — entry dropped lazily
```

## Requirements

- `KVStore(clock=None)` — `clock` defaults to `time.monotonic`
- `put(key, value, ttl=None)` — `ttl` seconds from now; `None` means forever
- `get` on expired key returns `None` and drops the entry
- `put` without `ttl` on an existing key clears ttl
