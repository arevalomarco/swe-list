#include "interview_test.hpp"
#include "cache.hpp"

TEST_CASE("tests/part2", "pin_protects_from_eviction") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  cache.put("c", 3);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("a") == 1);
  CHECK(cache.get("c") == 3);
}

TEST_CASE("tests/part2", "unpin_allows_eviction_again") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  cache.unpin("a");
  cache.get("b");
  cache.put("c", 3);
  CHECK(!cache.get("a").has_value());
  CHECK(cache.get("b") == 2);
  CHECK(cache.get("c") == 3);
}

TEST_CASE("tests/part2", "pin_missing_raises") {
  LRUCache cache(2);
  CHECK_THROWS(cache.pin("nope"));
}

TEST_CASE("tests/part2", "unpin_missing_or_unpinned_raises") {
  LRUCache cache(2);
  cache.put("a", 1);
  CHECK_THROWS(cache.unpin("a"));
  CHECK_THROWS(cache.unpin("nope"));
}

TEST_CASE("tests/part2", "put_when_all_pinned_raises") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  cache.pin("b");
  CHECK_THROWS(cache.put("c", 3));
}

TEST_CASE("tests/part2", "get_on_pinned_does_not_reorder_for_eviction") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  cache.get("a");
  cache.put("c", 3);
  CHECK(cache.get("a") == 1);
  CHECK(!cache.get("b").has_value());
}

TEST_CASE("tests/part2", "update_pinned_key_does_not_evict_it") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.pin("a");
  cache.put("a", 99);
  cache.put("c", 3);
  CHECK(cache.get("a") == 99);
  CHECK(!cache.get("b").has_value());
}
