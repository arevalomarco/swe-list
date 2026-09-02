import pytest

from solution.cache import Cache, LFUPolicy, LRUCache, LRUPolicy


def test_cache_defaults_to_lru_policy_when_none_given():
    cache = Cache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_cache_with_lfu_policy_evicts_least_frequent():
    cache = Cache(2, policy=LFUPolicy())
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)
    cache.put(3, 3)

    assert cache.get(2) is None
    assert cache.get(1) == 1
    assert cache.get(3) == 3


def test_swap_to_lfu_reseeds_so_next_eviction_unchanged():
    cache = Cache(2, policy=LRUPolicy())
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")

    cache.set_policy(LFUPolicy())
    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_swap_to_lru_reseeds_so_next_eviction_unchanged():
    cache = Cache(2, policy=LFUPolicy())
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")

    cache.set_policy(LRUPolicy())
    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_after_swap_later_accesses_follow_new_policy():
    cache = Cache(2, policy=LRUPolicy())
    cache.put("a", 1)
    cache.put("b", 2)

    cache.set_policy(LFUPolicy())
    cache.get("a")
    cache.get("a")
    cache.put("c", 3)

    assert cache.get("b") is None
    assert cache.get("a") == 1


def test_pin_excluded_from_policy_reseed_and_eviction():
    cache = Cache(2, policy=LRUPolicy())
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.set_policy(LFUPolicy())
    cache.put("c", 3)

    assert cache.get("a") == 1
    assert cache.get("b") is None
    assert cache.get("c") == 3


def test_lru_cache_still_supports_pin():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.pin("a")
    cache.put("c", 3)
    assert cache.get("a") == 1
    assert cache.get("b") is None


@pytest.mark.parametrize("capacity", [0, -1])
def test_cache_capacity_validated(capacity):
    with pytest.raises(ValueError):
        Cache(capacity)
