#pragma once

#include <functional>
#include <optional>
#include <stdexcept>
#include <string>

class KVStore {
 public:
  explicit KVStore(std::function<double()> clock = {}) {
    (void)clock;
    throw std::logic_error("not implemented");
  }

  void put(const std::string& key, int value, std::optional<double> ttl = std::nullopt) {
    (void)key;
    (void)value;
    (void)ttl;
    throw std::logic_error("not implemented");
  }

  std::optional<int> get(const std::string& key) {
    (void)key;
    throw std::logic_error("not implemented");
  }

  bool erase(const std::string& key) {
    (void)key;
    throw std::logic_error("not implemented");
  }

  using Callback = std::function<void(const std::string&, std::optional<int>)>;
  void watch(const std::string& key, Callback cb) {
    (void)key;
    (void)cb;
    throw std::logic_error("not implemented");
  }
  void unwatch(const std::string& key) {
    (void)key;
    throw std::logic_error("not implemented");
  }
  void expire_due(std::optional<double> now = std::nullopt) {
    (void)now;
    throw std::logic_error("not implemented");
  }
};
