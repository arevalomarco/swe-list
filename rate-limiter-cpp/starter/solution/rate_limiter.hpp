#pragma once

#include <functional>
#include <optional>
#include <stdexcept>
#include <string>

class RateLimiter {
 public:
  RateLimiter(int capacity, double window_seconds, std::function<double()> clock = {},
              std::optional<int> max_keys = std::nullopt) {
    (void)capacity;
    (void)window_seconds;
    (void)clock;
    (void)max_keys;
    throw std::logic_error("not implemented");
  }

  bool allow(const std::string& key = "default") {
    (void)key;
    throw std::logic_error("not implemented");
  }

  void set_limit(const std::string& key, int capacity) {
    (void)key;
    (void)capacity;
    throw std::logic_error("not implemented");
  }

  double retry_after(const std::string& key = "default") {
    (void)key;
    throw std::logic_error("not implemented");
  }
};
