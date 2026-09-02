#include "interview_test.hpp"
#include "event_log.hpp"

TEST_CASE("tests/part1", "empty_log_has_no_events") {
  EventLog log;
  CHECK(log.size() == 0);
  CHECK(log.all().empty());
}

TEST_CASE("tests/part1", "append_preserves_insertion_order") {
  EventLog log;
  log.append("trade", "px=101.5");
  log.append("quote", "bid=101.0");
  CHECK(log.size() == 2);
  const auto events = log.all();
  CHECK(events.size() == 2);
  CHECK(events[0].first == "trade");
  CHECK(events[0].second == "px=101.5");
  CHECK(events[1].first == "quote");
}

TEST_CASE("tests/part1", "duplicate_types_are_kept_separately") {
  EventLog log;
  log.append("trade", "1");
  log.append("trade", "2");
  CHECK(log.size() == 2);
  CHECK(log.all()[0].second == "1");
  CHECK(log.all()[1].second == "2");
}

TEST_CASE("tests/part1", "all_does_not_expose_internal_storage") {
  EventLog log;
  log.append("trade", "1");
  auto copy = log.all();
  copy.push_back({"injected", "999"});
  CHECK(log.size() == 1);
}
