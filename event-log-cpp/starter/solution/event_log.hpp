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
