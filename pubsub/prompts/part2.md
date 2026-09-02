# Pub / Sub — Part 2

Per-subscription bounded queues.

```python
s = bus.subscribe("t", capacity=1)
bus.publish("t", "a")  # 1
bus.publish("t", "b")  # 0 — s was full, dropped
```

## Requirements

- `subscribe(topic, capacity=None)` — `None` unbounded
- `publish` returns the number of subscribers that **accepted** the message
- If a bounded subscriber's queue is full, that subscriber drops (does not count as accepted)
