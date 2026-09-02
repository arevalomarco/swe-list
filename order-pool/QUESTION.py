"""
Order Pool, Part 1

Fixed-capacity pool of fixed-size blocks. No malloc on allocate after construction.

- OrderPool(block_size, capacity) — both positive integers; raise ValueError otherwise.
- allocate(thread=0) — mutable bytes-like of length block_size, or None if exhausted. thread unused here.
- release(block, thread=0) — return block to the pool. thread unused here.
- At most capacity live at once. Live allocations are distinct objects.

Example:
pool = OrderPool(block_size=8, capacity=2)
a = pool.allocate()
b = pool.allocate()
pool.allocate()  # None
pool.release(a)
pool.allocate()  # reuses a slot

"""
class OrderPool:
    def __init__(self, block_size, capacity):
        raise NotImplementedError

    def allocate(self, thread=0):
        """Return a block of `block_size` bytes, or None if the pool is exhausted."""
        raise NotImplementedError

    def release(self, block, thread=0):
        """Return `block` to the pool. `thread` is ignored until part 3."""
        raise NotImplementedError




"""
PART 2

Detect bad lifecycle.

- release of a block this pool currently considers free raises ValueError (double-free).
- release of an object this pool never returned from allocate raises ValueError.
- After a successful release, a later allocate may return that same object identity.
- Live allocations remain distinct.

Example:
pool = OrderPool(8, 2)
a = pool.allocate()
pool.release(a)
pool.release(a)         # ValueError
pool.release(object())  # ValueError

"""


"""
PART 3

Thread-local cache in front of a central free-list.

- OrderPool(block_size, capacity, cache_size=0) — cache_size non-negative; invalid → ValueError.
  cache_size == 0 is shared free-list (part 1/2 behaviour).
- allocate(thread=T): pop from T's cache if non-empty, else central. Both empty → None.
- release(block, thread=T): push onto T's cache if under cache_size, else spill to central.
- Double-free / unknown-block errors from part 2 still apply regardless of thread.

Example:
pool = OrderPool(8, 2, cache_size=2)
a = pool.allocate(thread=0)
b = pool.allocate(thread=0)
pool.release(a, thread=0)
pool.allocate(thread=1)       # None — cannot see thread 0's cache
pool.allocate(thread=0) is a  # True

"""
