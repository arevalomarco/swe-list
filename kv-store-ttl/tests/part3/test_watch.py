from solution.kv_store import KVStore


class FakeClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t
    def advance(self, dt):
        self.t += dt


def test_watch_put_delete():
    kv = KVStore()
    events = []
    kv.watch("a", lambda k, v: events.append((k, v)))
    kv.put("a", 2)
    kv.delete("a")
    assert events == [("a", 2), ("a", None)]


def test_watch_expiry_via_get():
    clock = FakeClock()
    kv = KVStore(clock=clock)
    events = []
    kv.watch("a", lambda k, v: events.append((k, v)))
    kv.put("a", 1, ttl=5)
    events.clear()
    clock.advance(5)
    assert kv.get("a") is None
    assert events == [("a", None)]


def test_expire_due():
    clock = FakeClock()
    kv = KVStore(clock=clock)
    events = []
    kv.watch("a", lambda k, v: events.append((k, v)))
    kv.put("a", 1, ttl=5)
    events.clear()
    clock.advance(5)
    kv.expire_due()
    assert events == [("a", None)]
    assert kv.get("a") is None


def test_unwatch():
    kv = KVStore()
    events = []
    cb = lambda k, v: events.append((k, v))
    kv.watch("a", cb)
    kv.unwatch("a", cb)
    kv.put("a", 1)
    assert events == []
