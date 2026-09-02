# Rate Limiter — Part 2

Per-key limits. Same window and capacity for every key.

```cpp
lim.allow("a");  // true
lim.allow("a");  // true
lim.allow("a");  // false
lim.allow("b");  // true
```

## Requirements

- `allow(key="default")` — independent budget per key.
- No-arg `allow()` still works (uses `"default"`).
