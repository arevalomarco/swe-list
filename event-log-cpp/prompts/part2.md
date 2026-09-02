# Event Log — Part 2

Query by type without scanning if you can index.

```cpp
log.by_type("trade");  // matching events in insertion order
log.by_type("fill");   // empty
```

## Requirements

- `by_type(event_type)` — insertion order; unknown type → empty vector
- Returned vector must not corrupt the log if mutated
- `append` must keep any index in sync
