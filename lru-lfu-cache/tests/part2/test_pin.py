import pytest

from solution.cache import LRUCache


def test_pin_protects_from_eviction():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_unpin_allows_eviction_again():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.unpin("a")
    cache.get("b")  # b is MRU among unpinned; a is LRU
    cache.put("c", 3)

    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_pin_missing_key_raises():
    cache = LRUCache(2)
    with pytest.raises(ValueError):
        cache.pin("nope")


def test_unpin_missing_or_unpinned_raises():
    cache = LRUCache(2)
    cache.put("a", 1)
    with pytest.raises(ValueError):
        cache.unpin("a")
    with pytest.raises(ValueError):
        cache.unpin("nope")


def test_put_when_all_pinned_raises():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.pin("b")
    with pytest.raises(ValueError):
        cache.put("c", 3)


def test_get_on_pinned_does_not_need_to_reorder_for_eviction():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.get("a")
    cache.put("c", 3)
    assert cache.get("a") == 1
    assert cache.get("b") is None


def test_update_pinned_key_does_not_evict_it():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.put("a", 99)
    cache.put("c", 3)
    assert cache.get("a") == 99
    assert cache.get("b") is None
