#include "interview_test.hpp"
#include "cache.hpp"

TEST_CASE("tests/part3", "cache_defaults_to_lru") {
  Cache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.get("a");
  cache.put("c", 3);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("a") == 1);
}

TEST_CASE("tests/part3", "lfu_evicts_least_frequent") {
  LFUPolicy policy;
  Cache cache(2, &policy);
  cache.put("1", 1);
  cache.put("2", 2);
  cache.get("1");
  cache.put("3", 3);
  CHECK(!cache.get("2").has_value());
  CHECK(cache.get("1") == 1);
  CHECK(cache.get("3") == 3);
}

TEST_CASE("tests/part3", "swap_to_lfu_preserves_next_eviction") {
  LRUPolicy lru;
  Cache cache(2, &lru);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.get("a");
  LFUPolicy lfu;
  cache.set_policy(&lfu);
  cache.put("c", 3);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("a") == 1);
}

TEST_CASE("tests/part3", "swap_to_lru_preserves_next_eviction") {
  LFUPolicy lfu;
  Cache cache(2, &lfu);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.get("a");
  LRUPolicy lru;
  cache.set_policy(&lru);
  cache.put("c", 3);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("a") == 1);
}

TEST_CASE("tests/part3", "after_swap_later_accesses_follow_new_policy") {
  LRUPolicy lru;
  Cache cache(2, &lru);
  cache.put("a", 1);
  cache.put("b", 2);
  LFUPolicy lfu;
  cache.set_policy(&lfu);
  cache.get("a");
  cache.get("a");
  cache.put("c", 3);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("a") == 1);
}

TEST_CASE("tests/part3", "pin_excluded_from_policy_reseed") {
  LRUPolicy lru;
  Cache cache(2, &lru);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  LFUPolicy lfu;
  cache.set_policy(&lfu);
  cache.put("c", 3);
  CHECK(cache.get("a") == 1);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("c") == 3);
}

TEST_CASE("tests/part3", "lru_cache_still_supports_pin") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  cache.put("c", 3);
  CHECK(cache.get("a") == 1);
  CHECK(!cache.get("b").has_value());
}

TEST_CASE("tests/part3", "cache_capacity_validated") {
  CHECK_THROWS(Cache(0));
  CHECK_THROWS(Cache(-1));
}
