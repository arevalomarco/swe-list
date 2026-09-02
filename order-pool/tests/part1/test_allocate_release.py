from solution.order_pool import OrderPool


def test_allocate_returns_a_block_of_the_requested_size():
    pool = OrderPool(8, 2)
    block = pool.allocate()

    assert block is not None
    assert len(block) == 8


def test_capacity_limits_live_blocks():
    pool = OrderPool(4, 2)
    a = pool.allocate()
    b = pool.allocate()

    assert a is not None and b is not None
    assert a is not b
    assert pool.allocate() is None


def test_release_makes_a_slot_available_again():
    pool = OrderPool(4, 1)
    a = pool.allocate()
    assert pool.allocate() is None
    pool.release(a)
    b = pool.allocate()
    assert b is not None
    assert len(b) == 4


def test_capacity_one():
    pool = OrderPool(1, 1)
    a = pool.allocate()
    assert len(a) == 1
    assert pool.allocate() is None
    pool.release(a)
    assert pool.allocate() is not None


def test_invalid_construction_raises():
    for args in ((0, 1), (1, 0), (-1, 2), (2, -1)):
        try:
            OrderPool(*args)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for OrderPool{args}")
