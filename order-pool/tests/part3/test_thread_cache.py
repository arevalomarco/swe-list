from solution.order_pool import OrderPool


def test_cached_release_is_invisible_to_another_thread():
    pool = OrderPool(8, 2, cache_size=2)
    a = pool.allocate(thread=0)
    b = pool.allocate(thread=0)
    assert a is not None and b is not None
    pool.release(a, thread=0)

    assert pool.allocate(thread=1) is None
    assert pool.allocate(thread=0) is a


def test_spill_to_central_is_visible_to_another_thread():
    pool = OrderPool(8, 2, cache_size=1)
    a = pool.allocate(thread=0)
    b = pool.allocate(thread=0)
    pool.release(a, thread=0)  # fills thread 0's cache
    pool.release(b, thread=0)  # cache full -> central

    c = pool.allocate(thread=1)
    assert c is b


def test_cache_size_zero_is_a_shared_freelist():
    pool = OrderPool(8, 1, cache_size=0)
    a = pool.allocate(thread=0)
    pool.release(a, thread=0)
    assert pool.allocate(thread=1) is a


def test_default_constructor_still_has_a_shared_freelist():
    pool = OrderPool(8, 1)
    a = pool.allocate()
    pool.release(a)
    assert pool.allocate(thread=1) is a


def test_double_free_across_threads_still_raises():
    pool = OrderPool(8, 2, cache_size=2)
    a = pool.allocate(thread=0)
    pool.release(a, thread=0)
    try:
        pool.release(a, thread=1)
    except ValueError:
        return
    raise AssertionError("expected ValueError on double-free from another thread")


def test_invalid_cache_size_raises():
    try:
        OrderPool(8, 2, cache_size=-1)
    except ValueError:
        return
    raise AssertionError("expected ValueError for negative cache_size")
