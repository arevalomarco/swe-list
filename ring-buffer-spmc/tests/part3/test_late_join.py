from solution.ring_buffer import RingBuffer


def test_late_consumer_does_not_see_history():
    rb = RingBuffer(2)
    early = rb.register_consumer()
    rb.push(1)
    rb.push(2)
    late = rb.register_consumer()
    assert late.pop() is None
    assert early.pop() == 1
    assert rb.push(3) is True
    assert late.pop() == 3
    assert early.pop() == 2


def test_unregister_frees_the_producer():
    rb = RingBuffer(1)
    stuck = rb.register_consumer()
    live = rb.register_consumer()
    assert rb.push(1) is True
    assert live.pop() == 1
    assert rb.push(2) is False
    stuck.unregister()
    assert rb.push(2) is True
    assert live.pop() == 2


def test_unregister_twice_raises():
    rb = RingBuffer(1)
    c = rb.register_consumer()
    c.unregister()
    try:
        c.unregister()
    except ValueError:
        return
    raise AssertionError("expected ValueError on a second unregister")


def test_pop_after_unregister_raises():
    rb = RingBuffer(2)
    c = rb.register_consumer()
    rb.push(1)
    c.unregister()
    try:
        c.pop()
    except ValueError:
        return
    raise AssertionError("expected ValueError when popping an unregistered consumer")


def test_unregister_last_consumer_makes_push_raise():
    rb = RingBuffer(2)
    c = rb.register_consumer()
    c.unregister()
    try:
        rb.push(1)
    except ValueError:
        return
    raise AssertionError("expected ValueError when pushing with no remaining consumer")
