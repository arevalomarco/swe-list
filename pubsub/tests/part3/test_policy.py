import pytest

from solution.pubsub import (
    BackpressureError,
    BlockStub,
    DropNewest,
    DropOldest,
    PubSub,
)


def test_drop_oldest_makes_room():
    bus = PubSub(policy=DropOldest())
    s = bus.subscribe("t", capacity=2)
    bus.publish("t", 1)
    bus.publish("t", 2)
    assert bus.publish("t", 3) == 1
    assert s.read() == 2
    assert s.read() == 3


def test_drop_newest_refuses():
    bus = PubSub(policy=DropNewest())
    s = bus.subscribe("t", capacity=1)
    bus.publish("t", 1)
    assert bus.publish("t", 2) == 0
    assert s.read() == 1


def test_block_stub_raises():
    bus = PubSub(policy=BlockStub())
    s = bus.subscribe("t", capacity=1)
    bus.publish("t", 1)
    with pytest.raises(BackpressureError):
        bus.publish("t", 2)
    assert s.read() == 1


def test_set_policy_applies_to_subsequent():
    bus = PubSub(policy=DropNewest())
    s = bus.subscribe("t", capacity=1)
    bus.publish("t", 1)
    bus.set_policy(DropOldest())
    assert bus.publish("t", 2) == 1
    assert s.read() == 2


def test_default_policy_is_drop_newest():
    bus = PubSub()
    s = bus.subscribe("t", capacity=1)
    bus.publish("t", 1)
    assert bus.publish("t", 2) == 0
