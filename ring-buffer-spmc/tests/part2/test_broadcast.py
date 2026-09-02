from solution.ring_buffer import RingBuffer


def test_every_value_is_delivered_to_every_consumer():
    rb = RingBuffer(4)
    c1 = rb.register_consumer()
    c2 = rb.register_consumer()
    rb.push(1)
    rb.push(2)
    assert c1.pop() == 1
    assert c2.pop() == 1
    assert c1.pop() == 2
    assert c2.pop() == 2
    assert c1.pop() is None
    assert c2.pop() is None


def test_slowest_consumer_keeps_the_buffer_full():
    rb = RingBuffer(2)
    slow = rb.register_consumer()
    fast = rb.register_consumer()
    assert rb.push(1) is True
    assert rb.push(2) is True
    assert fast.pop() == 1
    assert fast.pop() == 2
    assert rb.push(3) is False
    assert slow.pop() == 1
    assert rb.push(3) is True
    assert slow.pop() == 2
    assert fast.pop() == 3
    assert slow.pop() == 3


def test_three_consumers_independent_cursors():
    rb = RingBuffer(3)
    consumers = [rb.register_consumer() for _ in range(3)]
    for v in (10, 20, 30):
        assert rb.push(v) is True
    for c in consumers:
        assert [c.pop(), c.pop(), c.pop()] == [10, 20, 30]
        assert c.pop() is None
