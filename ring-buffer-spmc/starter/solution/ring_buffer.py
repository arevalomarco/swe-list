"""SPMC Ring Buffer — your implementation goes here."""


class Consumer:
    def pop(self):
        """Next value for this consumer, or None if it has nothing pending."""
        raise NotImplementedError


class RingBuffer:
    def __init__(self, capacity):
        raise NotImplementedError

    def push(self, value):
        """False if the buffer is full relative to the slowest consumer."""
        raise NotImplementedError

    def register_consumer(self):
        raise NotImplementedError
