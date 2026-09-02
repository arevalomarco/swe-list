# SPMC Ring Buffer — Part 3

Consumers can join late and leave.

- A consumer registered after pushes have happened starts at the current write position — empty until the next successful `push`.
- `Consumer.unregister()` — gone; no longer receives values and no longer counts toward full.
- Unregister twice / `pop` after unregister → `ValueError`.
- Unregistering the last consumer: further `push` raises `ValueError`.

Example:
```python
rb = RingBuffer(capacity=1)
stuck = rb.register_consumer()
live = rb.register_consumer()
rb.push(1)
live.pop()
rb.push(2)  # False
stuck.unregister()
rb.push(2)  # True
live.pop()  # 2
```
