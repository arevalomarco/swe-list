# Event Log — Part 1

Append-only in-memory log.

```python
log = EventLog()
log.append("trade", {"px": 101.5})
log.append("quote", {"bid": 101.0})
len(log)   # 2
log.all()  # [("trade", {"px": 101.5}), ("quote", {"bid": 101.0})]
```

## Requirements

- `append(event_type, payload) -> None`
- `all() -> list[tuple]` — insertion order; must not expose mutable internal storage
- `len(log)` — event count

Implement in `solution/event_log.py`.
