"""
SPMC Ring Buffer, Part 1

Fixed-capacity ring. One producer, one consumer. Do not use collections.deque — wrap the indices yourself.

- RingBuffer(capacity) — positive integer; raise ValueError otherwise.
- register_consumer() -> Consumer — keep the registration API (part 2 registers more).
- push(value) -> bool — True if stored, False if full. Pushing with no consumer raises ValueError.
- Consumer.pop() — next value in FIFO order, or None if caught up.

Example:
rb = RingBuffer(capacity=3)
c = rb.register_consumer()
rb.push(1); rb.push(2)
c.pop()  # 1
c.pop()  # 2
c.pop()  # None
rb.push(3); rb.push(4); rb.push(5)
rb.push(6)  # False

"""
class Consumer:
    def pop(self):
        """Next value for this consumer, or None if it has nothing pending."""
        raise NotImplementedError


class RingBuffer:
    def __init__(self, capacity):
        raise NotImplementedError

    def push(self, value):
        """False if the buffer is full relative to the slowest consumer."""
        raise NotImplementedError

    def register_consumer(self):
        raise NotImplementedError




"""
PART 2

Several consumers, each reading independently. Broadcast: every push is delivered once per registered consumer, in order.

- register_consumer() may be called any number of times. Each Consumer has its own read position.
- push returns False when any still-registered consumer is capacity behind (slowest consumer wins).
- One ring of slots, many read indices — not a private queue per consumer.

Example:
rb = RingBuffer(capacity=4)
c1 = rb.register_consumer()
c2 = rb.register_consumer()
rb.push(1); rb.push(2)
c1.pop()  # 1
c2.pop()  # 1
c1.pop()  # 2
c2.pop()  # 2

"""


"""
PART 3

Consumers can join late and leave.

- A consumer registered after pushes have happened starts at the current write position — empty until the next successful push.
- Consumer.unregister() — gone; no longer receives values and no longer counts toward full.
- Unregister twice / pop after unregister → ValueError.
- Unregistering the last consumer: further push raises ValueError.

Example:
rb = RingBuffer(capacity=1)
stuck = rb.register_consumer()
live = rb.register_consumer()
rb.push(1)
live.pop()
rb.push(2)  # False
stuck.unregister()
rb.push(2)  # True
live.pop()  # 2

"""
