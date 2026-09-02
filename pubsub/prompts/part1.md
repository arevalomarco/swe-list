# Pub / Sub — Part 1

In-process topics.

```python
bus = PubSub()
s = bus.subscribe("trades")
bus.publish("trades", {"px": 1})
s.read()  # {"px": 1}
s.read()  # None
```

## Requirements

- `PubSub()`
- `subscribe(topic) -> Subscription` with `read() -> message | None`
- `publish(topic, message)` delivers a **copy** to every current subscriber
- `Subscription.unsubscribe()` — further `read` raises `ValueError`

Implement in `solution/pubsub.py`.
