# KV Store + TTL — Part 1

```python
kv = KVStore()
kv.put("a", 1)
kv.get("a")     # 1
kv.delete("a")  # True
kv.get("a")     # None
```

## Requirements

- `KVStore()`
- `put(key, value)`
- `get(key) -> value | None`
- `delete(key) -> bool`

Implement in `solution/kv_store.py`.
