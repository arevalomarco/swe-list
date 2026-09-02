#include "interview_test.hpp"
#include "kv_store.hpp"

TEST_CASE("tests/part1", "put_get_erase") {
  KVStore kv;
  kv.put("a", 1);
  CHECK(kv.get("a") == 1);
  CHECK(kv.erase("a") == true);
  CHECK(!kv.get("a").has_value());
}

TEST_CASE("tests/part1", "get_missing") {
  CHECK(!KVStore().get("nope").has_value());
}

TEST_CASE("tests/part1", "erase_missing") {
  CHECK(KVStore().erase("nope") == false);
}

TEST_CASE("tests/part1", "overwrite") {
  KVStore kv;
  kv.put("a", 1);
  kv.put("a", 2);
  CHECK(kv.get("a") == 2);
}
