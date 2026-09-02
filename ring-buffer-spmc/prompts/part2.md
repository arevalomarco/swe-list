# SPMC Ring Buffer — Part 2

Several consumers, each reading independently. Broadcast: every `push` is delivered once per registered consumer, in order.

- `register_consumer()` may be called any number of times. Each `Consumer` has its own read position.
- `push` returns `False` when any still-registered consumer is `capacity` behind (slowest consumer wins).
- One ring of slots, many read indices — not a private queue per consumer.

Example:
```python
rb = RingBuffer(capacity=4)
c1 = rb.register_consumer()
c2 = rb.register_consumer()
rb.push(1); rb.push(2)
c1.pop()  # 1
c2.pop()  # 1
c1.pop()  # 2
c2.pop()  # 2
```
