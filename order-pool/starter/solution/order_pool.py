"""Order Pool — your implementation goes here."""


class OrderPool:
    def __init__(self, block_size, capacity):
        raise NotImplementedError

    def allocate(self, thread=0):
        """Return a block of `block_size` bytes, or None if the pool is exhausted."""
        raise NotImplementedError

    def release(self, block, thread=0):
        """Return `block` to the pool. `thread` is ignored until part 3."""
        raise NotImplementedError
