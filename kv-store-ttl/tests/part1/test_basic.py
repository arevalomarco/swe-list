from solution.kv_store import KVStore


def test_put_get_delete():
    kv = KVStore()
    kv.put("a", 1)
    assert kv.get("a") == 1
    assert kv.delete("a") is True
    assert kv.get("a") is None


def test_get_missing():
    kv = KVStore()
    assert kv.get("nope") is None


def test_delete_missing():
    kv = KVStore()
    assert kv.delete("nope") is False


def test_overwrite():
    kv = KVStore()
    kv.put("a", 1)
    kv.put("a", 2)
    assert kv.get("a") == 2
