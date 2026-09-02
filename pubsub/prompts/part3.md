# Pub / Sub — Part 3

Backpressure policy on publish.

```python
bus = PubSub(policy=DropOldest())
# or DropNewest(), or BlockStub() which raises BackpressureError when any bounded sub is full
bus.set_policy(DropNewest())  # applies to subsequent publishes only
```

## Requirements

- `PubSub(policy=None)` — default behaves like part 2 (drop newest / refuse when full)
- Policies: `DropNewest`, `DropOldest`, `BlockStub`
  - `DropOldest`: when full, drop oldest queued message then enqueue
  - `DropNewest`: when full, refuse the new message (part-2 default)
  - `BlockStub`: raise `BackpressureError` instead of dropping when any bounded sub is full
- `set_policy(policy)` at runtime; existing queues unchanged
