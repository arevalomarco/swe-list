"""KV Store + TTL — your implementation goes here."""


class KVStore:
    def __init__(self, clock=None):
        raise NotImplementedError

    def put(self, key, value, ttl=None):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def watch(self, key, callback):
        raise NotImplementedError

    def unwatch(self, key, callback):
        raise NotImplementedError

    def expire_due(self, now=None):
        raise NotImplementedError
