/*
Event Log, Part 1

Append-only in-memory log.

EventLog log;
log.append("trade", "px=101.5");
log.append("quote", "bid=101.0");
log.size();   // 2
log.all();    // {{"trade", "px=101.5"}, {"quote", "bid=101.0"}}

- append(event_type, payload) — payload is std::string
- all() — insertion order; must not expose mutable internal storage (return by value)
- size() — event count
- EventLog(std::optional<std::size_t> capacity = nullopt) — part 1 ignores capacity

*/
#pragma once

#include <cstddef>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class EventLog {
 public:
  explicit EventLog(std::optional<std::size_t> capacity = std::nullopt) {
    (void)capacity;
    throw std::logic_error("not implemented");
  }

  void append(const std::string& event_type, const std::string& payload) {
    (void)event_type;
    (void)payload;
    throw std::logic_error("not implemented");
  }

  std::vector<std::pair<std::string, std::string>> all() const {
    throw std::logic_error("not implemented");
  }

  std::vector<std::pair<std::string, std::string>> by_type(const std::string& event_type) const {
    (void)event_type;
    throw std::logic_error("not implemented");
  }

  std::size_t size() const { throw std::logic_error("not implemented"); }
};



/*
PART 2

Query by type without scanning if you can index.

log.by_type("trade");  // matching events in insertion order
log.by_type("fill");   // empty

- by_type(event_type) — insertion order; unknown type → empty vector
- Returned vector must not corrupt the log if mutated
- append must keep any index in sync

*/


/*
PART 3

Bounded log; oldest events drop when over capacity.

EventLog log(2);
log.append("trade", "1");
log.append("trade", "2");
log.append("quote", "3");  // evicts ("trade", "1")
log.size();                // 2
log.by_type("trade");      // {{"trade", "2"}}

- EventLog(capacity) — nullopt unbounded; throw std::invalid_argument if capacity < 1
- At capacity, append evicts the oldest event
- by_type must never return an evicted event

*/
