# Token Manager — Part 1

Fixed `time_to_live` at construction. Times only increase. Expire lazily — no background thread.

```python
mgr = TokenManager(5)
mgr.generate("t1", 1)
mgr.renew("t1", 2)
mgr.count_unexpired(6)  # 1
mgr.count_unexpired(8)  # 0
```

## Requirements

- `TokenManager(time_to_live)`
- `generate(token_id, current_time)` — expires at `current_time + time_to_live` (re-generate resets)
- `renew(token_id, current_time)` — no-op if missing or already expired; else extend from `current_time`
- `count_unexpired(current_time) -> int`

Implement in `solution/token_manager.py`.
