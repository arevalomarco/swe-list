# Event Log — Part 3

Bounded log; oldest events drop when over capacity.

```cpp
EventLog log(2);
log.append("trade", "1");
log.append("trade", "2");
log.append("quote", "3");  // evicts ("trade", "1")
log.size();                // 2
log.by_type("trade");      // {{"trade", "2"}}
```

## Requirements

- `EventLog(capacity)` — `nullopt` unbounded; throw `std::invalid_argument` if `capacity < 1`
- At capacity, append evicts the oldest event
- `by_type` must never return an evicted event
