#include "interview_test.hpp"
#include "event_log.hpp"

TEST_CASE("tests/part2", "by_type_returns_only_matching_events") {
  EventLog log;
  log.append("trade", "1");
  log.append("quote", "2");
  log.append("trade", "3");
  CHECK(log.by_type("trade").size() == 2);
  CHECK(log.by_type("trade")[0].second == "1");
  CHECK(log.by_type("trade")[1].second == "3");
  CHECK(log.by_type("quote").size() == 1);
}

TEST_CASE("tests/part2", "unknown_type_returns_empty") {
  EventLog log;
  log.append("trade", "1");
  CHECK(log.by_type("fill").empty());
}

TEST_CASE("tests/part2", "by_type_on_empty_log") {
  CHECK(EventLog().by_type("trade").empty());
}

TEST_CASE("tests/part2", "by_type_does_not_expose_internal_storage") {
  EventLog log;
  log.append("trade", "1");
  auto copy = log.by_type("trade");
  copy.push_back({"injected", "999"});
  CHECK(log.by_type("trade").size() == 1);
}
