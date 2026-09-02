from solution.ring_buffer import RingBuffer


def test_push_then_pop_is_fifo():
    rb = RingBuffer(3)
    c = rb.register_consumer()
    assert rb.push(1) is True
    assert rb.push(2) is True
    assert c.pop() == 1
    assert c.pop() == 2
    assert c.pop() is None


def test_pop_on_empty_returns_none():
    rb = RingBuffer(2)
    c = rb.register_consumer()
    assert c.pop() is None


def test_push_on_full_returns_false():
    rb = RingBuffer(2)
    c = rb.register_consumer()
    assert rb.push(1) is True
    assert rb.push(2) is True
    assert rb.push(3) is False
    assert c.pop() == 1
    assert rb.push(3) is True
    assert c.pop() == 2
    assert c.pop() == 3


def test_wraparound_over_several_cycles():
    rb = RingBuffer(2)
    c = rb.register_consumer()
    for i in range(10):
        assert rb.push(i) is True
        assert c.pop() == i


def test_capacity_one():
    rb = RingBuffer(1)
    c = rb.register_consumer()
    assert rb.push("x") is True
    assert rb.push("y") is False
    assert c.pop() == "x"
    assert rb.push("y") is True
    assert c.pop() == "y"


def test_push_before_a_consumer_raises():
    rb = RingBuffer(2)
    try:
        rb.push(1)
    except ValueError:
        return
    raise AssertionError("expected ValueError when pushing with no consumer")


def test_invalid_capacity_raises():
    for cap in (0, -1):
        try:
            RingBuffer(cap)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for capacity={cap}")
