"""
KV Store + TTL, Part 1

kv = KVStore()
kv.put("a", 1)
kv.get("a")     # 1
kv.delete("a")  # True
kv.get("a")     # None

- KVStore()
- put(key, value)
- get(key) -> value | None
- delete(key) -> bool

"""
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




"""
PART 2

kv = KVStore(clock=fake)
kv.put("a", 1, ttl=10)
# after 10s...
kv.get("a")  # None — entry dropped lazily

- KVStore(clock=None) — clock defaults to time.monotonic
- put(key, value, ttl=None) — ttl seconds from now; None means forever
- get on expired key returns None and drops the entry
- put without ttl on an existing key clears ttl

"""


"""
PART 3

Watchers.

def cb(key, new_value): ...
kv.watch("a", cb)
kv.put("a", 2)       # cb("a", 2)
kv.delete("a")       # cb("a", None)
kv.expire_due(now)   # notifies watchers for newly discovered expiries

- watch(key, callback) / unwatch(key, callback)
- callback(key, new_value_or_None) on put/delete/expiry
- Expiry must notify when discovered via get or expire_due(now)

"""
