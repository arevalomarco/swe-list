# Event Log — Part 1

Append-only in-memory log.

```cpp
EventLog log;
log.append("trade", "px=101.5");
log.append("quote", "bid=101.0");
log.size();   // 2
log.all();    // {{"trade", "px=101.5"}, {"quote", "bid=101.0"}}
```

## Requirements

- `append(event_type, payload)` — `payload` is `std::string`
- `all()` — insertion order; must not expose mutable internal storage (return by value)
- `size()` — event count
- `EventLog(std::optional<std::size_t> capacity = nullopt)` — part 1 ignores capacity

Implement in `solution/event_log.hpp`.
