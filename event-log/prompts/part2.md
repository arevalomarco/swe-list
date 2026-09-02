# Event Log — Part 2

Query by type without scanning if you can index.

```python
log.by_type("trade")  # [("trade", {"px": 101.5})]
log.by_type("fill")   # []
```

## Requirements

- `by_type(event_type) -> list[tuple]` — insertion order; unknown type -> `[]`
- Returned list must not corrupt the log if mutated
- `append` must keep any index in sync
