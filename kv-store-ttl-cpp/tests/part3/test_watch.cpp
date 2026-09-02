#include "interview_test.hpp"
#include "kv_store.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part3", "watch_put_erase") {
  KVStore kv;
  std::vector<std::pair<std::string, std::optional<int>>> events;
  kv.watch("a", [&](const std::string& k, std::optional<int> v) { events.push_back({k, v}); });
  kv.put("a", 2);
  kv.erase("a");
  CHECK(events.size() == 2);
  CHECK(events[0].second == 2);
  CHECK(!events[1].second.has_value());
}

TEST_CASE("tests/part3", "watch_expiry_via_get") {
  FakeClock clock;
  KVStore kv([&clock] { return clock(); });
  std::vector<std::optional<int>> events;
  kv.watch("a", [&](const std::string&, std::optional<int> v) { events.push_back(v); });
  kv.put("a", 1, 5);
  events.clear();
  clock.advance(5);
  CHECK(!kv.get("a").has_value());
  CHECK(events.size() == 1);
  CHECK(!events[0].has_value());
}

TEST_CASE("tests/part3", "expire_due") {
  FakeClock clock;
  KVStore kv([&clock] { return clock(); });
  std::vector<std::optional<int>> events;
  kv.watch("a", [&](const std::string&, std::optional<int> v) { events.push_back(v); });
  kv.put("a", 1, 5);
  events.clear();
  clock.advance(5);
  kv.expire_due();
  CHECK(events.size() == 1);
  CHECK(!kv.get("a").has_value());
}

TEST_CASE("tests/part3", "unwatch") {
  KVStore kv;
  std::vector<int> events;
  kv.watch("a", [&](const std::string&, std::optional<int>) { events.push_back(1); });
  kv.unwatch("a");
  kv.put("a", 1);
  CHECK(events.empty());
}
