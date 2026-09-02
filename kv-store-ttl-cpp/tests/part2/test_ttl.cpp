#include "interview_test.hpp"
#include "kv_store.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part2", "ttl_expires") {
  FakeClock clock;
  KVStore kv([&clock] { return clock(); });
  kv.put("a", 1, 10);
  CHECK(kv.get("a") == 1);
  clock.advance(10);
  CHECK(!kv.get("a").has_value());
}

TEST_CASE("tests/part2", "put_without_ttl_clears") {
  FakeClock clock;
  KVStore kv([&clock] { return clock(); });
  kv.put("a", 1, 5);
  kv.put("a", 2);
  clock.advance(100);
  CHECK(kv.get("a") == 2);
}

TEST_CASE("tests/part2", "forever_default") {
  FakeClock clock;
  KVStore kv([&clock] { return clock(); });
  kv.put("a", 1);
  clock.advance(1000);
  CHECK(kv.get("a") == 1);
}
