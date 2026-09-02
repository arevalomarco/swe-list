import pytest

from solution.cache import LRUCache


def test_put_then_get_returns_the_value():
    cache = LRUCache(2)
    cache.put("a", 1)

    assert cache.get("a") == 1


def test_get_on_a_missing_key_returns_none():
    cache = LRUCache(2)

    assert cache.get("nope") is None


def test_the_worked_example_evicts_the_least_recently_used_key():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1  # "a" is now the most recently used

    cache.put("c", 3)  # cache full; "b" is the least recently used -> evicted

    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_get_marks_a_key_as_most_recently_used():
    cache = LRUCache(2)
    cache.put(1, "x")
    cache.put(2, "y")
    cache.get(1)        # touches 1 — 2 is now the least recently used
    cache.put(3, "z")   # evicts 2, not 1

    assert cache.get(2) is None
    assert cache.get(1) == "x"


def test_put_on_an_existing_key_updates_the_value_and_counts_as_a_use():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 100)  # update — "b" is now the least recently used
    cache.put("c", 3)     # evicts "b"

    assert cache.get("a") == 100
    assert cache.get("b") is None


def test_capacity_one_evicts_on_every_new_key():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.put("b", 2)  # evicts "a"

    assert cache.get("a") is None
    assert cache.get("b") == 2


def test_put_does_not_evict_when_under_capacity():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)

    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_updating_a_key_does_not_change_how_many_entries_are_cached():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 999)  # update, not a new entry
    cache.put("c", 3)     # still only evicts one entry ("b")

    assert cache.get("a") == 999
    assert cache.get("c") == 3
    assert cache.get("b") is None


def test_eviction_order_across_a_longer_sequence_of_puts_and_gets():
    cache = LRUCache(2)
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1)         # order: 2 (LRU), 1 (MRU)
    cache.put(3, "c")     # evicts 2 — order: 1, 3
    cache.get(1)         # order: 3 (LRU), 1 (MRU)
    cache.put(4, "d")     # evicts 3 — order: 1, 4

    assert cache.get(2) is None
    assert cache.get(3) is None
    assert cache.get(1) == "a"
    assert cache.get(4) == "d"


@pytest.mark.parametrize("capacity", [0, -1])
def test_non_positive_capacity_is_rejected(capacity):
    with pytest.raises(ValueError):
        LRUCache(capacity)
