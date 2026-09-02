from solution.kv_store import KVStore


class FakeClock:
    def __init__(self):
        self.t = 0.0
    def __call__(self):
        return self.t
    def advance(self, dt):
        self.t += dt


def test_ttl_expires():
    clock = FakeClock()
    kv = KVStore(clock=clock)
    kv.put("a", 1, ttl=10)
    assert kv.get("a") == 1
    clock.advance(10)
    assert kv.get("a") is None


def test_put_without_ttl_clears():
    clock = FakeClock()
    kv = KVStore(clock=clock)
    kv.put("a", 1, ttl=5)
    kv.put("a", 2)
    clock.advance(100)
    assert kv.get("a") == 2


def test_forever_default():
    clock = FakeClock()
    kv = KVStore(clock=clock)
    kv.put("a", 1)
    clock.advance(1000)
    assert kv.get("a") == 1
