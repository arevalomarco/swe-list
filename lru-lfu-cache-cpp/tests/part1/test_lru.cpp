#include "interview_test.hpp"
#include "cache.hpp"

TEST_CASE("tests/part1", "put_then_get") {
  LRUCache cache(2);
  cache.put("a", 1);
  CHECK(cache.get("a") == 1);
}

TEST_CASE("tests/part1", "get_missing") {
  LRUCache cache(2);
  CHECK(!cache.get("nope").has_value());
}

TEST_CASE("tests/part1", "evicts_least_recently_used") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  CHECK(cache.get("a") == 1);
  cache.put("c", 3);
  CHECK(!cache.get("b").has_value());
  CHECK(cache.get("a") == 1);
  CHECK(cache.get("c") == 3);
}

TEST_CASE("tests/part1", "get_marks_as_mru") {
  LRUCache cache(2);
  cache.put("1", 10);
  cache.put("2", 20);
  cache.get("1");
  cache.put("3", 30);
  CHECK(!cache.get("2").has_value());
  CHECK(cache.get("1") == 10);
}

TEST_CASE("tests/part1", "put_update_counts_as_use") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.put("a", 100);
  cache.put("c", 3);
  CHECK(cache.get("a") == 100);
  CHECK(!cache.get("b").has_value());
}

TEST_CASE("tests/part1", "capacity_one") {
  LRUCache cache(1);
  cache.put("a", 1);
  cache.put("b", 2);
  CHECK(!cache.get("a").has_value());
  CHECK(cache.get("b") == 2);
}

TEST_CASE("tests/part1", "update_does_not_grow") {
  LRUCache cache(2);
  cache.put("a", 1);
  cache.put("b", 2);
  cache.put("a", 999);
  cache.put("c", 3);
  CHECK(cache.get("a") == 999);
  CHECK(cache.get("c") == 3);
  CHECK(!cache.get("b").has_value());
}

TEST_CASE("tests/part1", "non_positive_capacity") {
  CHECK_THROWS(LRUCache(0));
  CHECK_THROWS(LRUCache(-1));
}
