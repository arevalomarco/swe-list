"""
Pub / Sub, Part 1

In-process topics.

bus = PubSub()
s = bus.subscribe("trades")
bus.publish("trades", {"px": 1})
s.read()  # {"px": 1}
s.read()  # None

- PubSub()
- subscribe(topic) -> Subscription with read() -> message | None
- publish(topic, message) delivers a copy to every current subscriber
- Subscription.unsubscribe() — further read raises ValueError

"""
class PubSub:
    def __init__(self, policy=None):
        raise NotImplementedError

    def subscribe(self, topic, capacity=None):
        raise NotImplementedError

    def publish(self, topic, message):
        raise NotImplementedError

    def set_policy(self, policy):
        raise NotImplementedError




"""
PART 2

Per-subscription bounded queues.

s = bus.subscribe("t", capacity=1)
bus.publish("t", "a")  # 1
bus.publish("t", "b")  # 0 — s was full, dropped

- subscribe(topic, capacity=None) — None unbounded
- publish returns the number of subscribers that accepted the message
- If a bounded subscriber's queue is full, that subscriber drops (does not count as accepted)

"""


"""
PART 3

Backpressure policy on publish.

bus = PubSub(policy=DropOldest())
# or DropNewest(), or BlockStub() which raises BackpressureError when any bounded sub is full
bus.set_policy(DropNewest())  # applies to subsequent publishes only

- PubSub(policy=None) — default behaves like part 2 (drop newest / refuse when full)
- Policies: DropNewest, DropOldest, BlockStub
  - DropOldest: when full, drop oldest queued message then enqueue
  - DropNewest: when full, refuse the new message (part-2 default)
  - BlockStub: raise BackpressureError instead of dropping when any bounded sub is full
- set_policy(policy) at runtime; existing queues unchanged

"""
