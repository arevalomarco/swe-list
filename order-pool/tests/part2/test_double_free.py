from solution.order_pool import OrderPool


def test_double_free_raises():
    pool = OrderPool(8, 2)
    a = pool.allocate()
    pool.release(a)
    try:
        pool.release(a)
    except ValueError:
        return
    raise AssertionError("expected ValueError on double-free")


def test_release_of_an_unknown_block_raises():
    pool = OrderPool(8, 2)
    pool.allocate()
    try:
        pool.release(object())
    except ValueError:
        return
    raise AssertionError("expected ValueError for a block this pool never handed out")


def test_released_block_may_be_the_next_allocate():
    pool = OrderPool(8, 1)
    a = pool.allocate()
    pool.release(a)
    b = pool.allocate()
    assert b is a


def test_live_blocks_stay_distinct_after_a_recycle():
    pool = OrderPool(4, 2)
    a = pool.allocate()
    b = pool.allocate()
    pool.release(a)
    c = pool.allocate()
    assert c is not b
    assert len(c) == 4
