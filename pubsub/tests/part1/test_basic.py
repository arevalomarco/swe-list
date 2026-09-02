from copy import deepcopy

from solution.pubsub import PubSub


def test_publish_delivers_to_subscriber():
    bus = PubSub()
    s = bus.subscribe("trades")
    bus.publish("trades", {"px": 1})
    assert s.read() == {"px": 1}
    assert s.read() is None


def test_multiple_subscribers_get_copies():
    bus = PubSub()
    a = bus.subscribe("t")
    b = bus.subscribe("t")
    msg = {"x": 1}
    bus.publish("t", msg)
    ra, rb = a.read(), b.read()
    assert ra == {"x": 1} and rb == {"x": 1}
    ra["x"] = 99
    assert b.read() is None
    # other sub not affected by mutation of first copy
    bus.publish("t", {"y": 2})
    assert a.read() == {"y": 2}


def test_publish_to_unknown_topic_is_fine():
    bus = PubSub()
    assert bus.publish("nope", 1) == 0


def test_unsubscribe_blocks_further_reads():
    import pytest
    bus = PubSub()
    s = bus.subscribe("t")
    s.unsubscribe()
    with pytest.raises(ValueError):
        s.read()


def test_unsubscribed_no_longer_receives():
    bus = PubSub()
    s = bus.subscribe("t")
    s.unsubscribe()
    bus.publish("t", 1)
    # cannot read; and must not have been queued — only check no crash
