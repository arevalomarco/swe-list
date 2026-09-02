# SPMC Ring Buffer — Part 1

Fixed-capacity ring. One producer, one consumer. Do not use `collections.deque` — wrap the indices yourself.

- `RingBuffer(capacity)` — positive integer; raise `ValueError` otherwise.
- `register_consumer() -> Consumer` — keep the registration API (part 2 registers more).
- `push(value) -> bool` — `True` if stored, `False` if full. Pushing with no consumer raises `ValueError`.
- `Consumer.pop()` — next value in FIFO order, or `None` if caught up.

Example:
```python
rb = RingBuffer(capacity=3)
c = rb.register_consumer()
rb.push(1); rb.push(2)
c.pop()  # 1
c.pop()  # 2
c.pop()  # None
rb.push(3); rb.push(4); rb.push(5)
rb.push(6)  # False
```
