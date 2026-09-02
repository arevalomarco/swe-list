# Token Manager — Part 3

Leases with fencing tokens.

```python
f = mgr.acquire("res", "h1", 0)   # fence int
mgr.renew_lease("res", "h1", f, 1)  # True
mgr.acquire("res", "h2", 1)         # None — still held
# after expiry, new acquire returns a strictly larger fence
```

## Requirements

- `acquire(resource_id, holder_id, current_time) -> fence | None` — None if held by another unexpired lease
- Same holder re-acquire while held renews and returns the **same** fence
- `renew_lease(resource_id, holder_id, fence, current_time) -> bool` — wrong fence/holder -> False
- New acquire after expiry returns a strictly larger fence than any prior lease on that resource
