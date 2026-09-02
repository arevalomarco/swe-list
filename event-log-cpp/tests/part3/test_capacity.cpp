#include "interview_test.hpp"
#include "event_log.hpp"

TEST_CASE("tests/part3", "capacity_none_is_unbounded") {
  EventLog log;
  for (int i = 0; i < 50; ++i) log.append("trade", std::to_string(i));
  CHECK(log.size() == 50);
}

TEST_CASE("tests/part3", "oldest_event_is_evicted_at_capacity") {
  EventLog log(2);
  log.append("trade", "1");
  log.append("trade", "2");
  log.append("quote", "3");
  CHECK(log.size() == 2);
  CHECK(log.all()[0].first == "trade");
  CHECK(log.all()[0].second == "2");
  CHECK(log.all()[1].first == "quote");
}

TEST_CASE("tests/part3", "eviction_updates_type_lookup") {
  EventLog log(2);
  log.append("trade", "1");
  log.append("trade", "2");
  log.append("quote", "3");
  CHECK(log.by_type("trade").size() == 1);
  CHECK(log.by_type("trade")[0].second == "2");
}

TEST_CASE("tests/part3", "type_disappears_once_all_its_events_are_evicted") {
  EventLog log(1);
  log.append("trade", "1");
  log.append("quote", "2");
  CHECK(log.by_type("trade").empty());
  CHECK(log.by_type("quote").size() == 1);
}

TEST_CASE("tests/part3", "capacity_below_one_is_rejected") {
  CHECK_THROWS(EventLog(0));
}
