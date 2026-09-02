"""Circuit Breaker — your implementation goes here."""


class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold, cool_down_seconds, clock=None, policy=None):
        raise NotImplementedError

    def call(self, fn, *args, **kwargs):
        raise NotImplementedError

    def set_policy(self, policy):
        raise NotImplementedError
