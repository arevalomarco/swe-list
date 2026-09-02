"""Pub / Sub — your implementation goes here."""


class PubSub:
    def __init__(self, policy=None):
        raise NotImplementedError

    def subscribe(self, topic, capacity=None):
        raise NotImplementedError

    def publish(self, topic, message):
        raise NotImplementedError

    def set_policy(self, policy):
        raise NotImplementedError
