from solution.pubsub import PubSub


def test_publish_returns_accept_count():
    bus = PubSub()
    a = bus.subscribe("t", capacity=1)
    b = bus.subscribe("t", capacity=1)
    assert bus.publish("t", "a") == 2
    assert bus.publish("t", "b") == 0  # both full


def test_full_subscriber_drops_others_still_accept():
    bus = PubSub()
    bounded = bus.subscribe("t", capacity=1)
    unbounded = bus.subscribe("t")
    bus.publish("t", 1)
    assert bus.publish("t", 2) == 1  # only unbounded
    assert bounded.read() == 1
    assert unbounded.read() == 1
    assert unbounded.read() == 2


def test_unbounded_never_drops():
    bus = PubSub()
    s = bus.subscribe("t")
    for i in range(20):
        assert bus.publish("t", i) == 1
    assert [s.read() for _ in range(20)] == list(range(20))


def test_capacity_zero_never_accepts():
    bus = PubSub()
    s = bus.subscribe("t", capacity=0)
    assert bus.publish("t", 1) == 0
    assert s.read() is None


def test_part1_still_works():
    bus = PubSub()
    s = bus.subscribe("trades")
    bus.publish("trades", {"px": 1})
    assert s.read() == {"px": 1}
