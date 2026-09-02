#pragma once

#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

class EvictionPolicy {
 public:
  virtual ~EvictionPolicy() = default;
  virtual void touch(const std::string& key) = 0;
  virtual void forget(const std::string& key) = 0;
  virtual std::string evict() = 0;
  virtual std::vector<std::string> ordered_keys() const = 0;
  virtual void reset(const std::vector<std::string>& keys_most_evictable_first) = 0;
};

class LRUPolicy : public EvictionPolicy {
 public:
  void touch(const std::string&) override { throw std::logic_error("not implemented"); }
  void forget(const std::string&) override { throw std::logic_error("not implemented"); }
  std::string evict() override { throw std::logic_error("not implemented"); }
  std::vector<std::string> ordered_keys() const override { throw std::logic_error("not implemented"); }
  void reset(const std::vector<std::string>&) override { throw std::logic_error("not implemented"); }
};

class LFUPolicy : public EvictionPolicy {
 public:
  void touch(const std::string&) override { throw std::logic_error("not implemented"); }
  void forget(const std::string&) override { throw std::logic_error("not implemented"); }
  std::string evict() override { throw std::logic_error("not implemented"); }
  std::vector<std::string> ordered_keys() const override { throw std::logic_error("not implemented"); }
  void reset(const std::vector<std::string>&) override { throw std::logic_error("not implemented"); }
};

class Cache {
 public:
  explicit Cache(int capacity, EvictionPolicy* policy = nullptr) {
    (void)capacity;
    (void)policy;
    throw std::logic_error("not implemented");
  }
  std::optional<int> get(const std::string&) { throw std::logic_error("not implemented"); }
  void put(const std::string&, int) { throw std::logic_error("not implemented"); }
  void pin(const std::string&) { throw std::logic_error("not implemented"); }
  void unpin(const std::string&) { throw std::logic_error("not implemented"); }
  void set_policy(EvictionPolicy*) { throw std::logic_error("not implemented"); }
};

class LRUCache {
 public:
  explicit LRUCache(int capacity) { (void)capacity; throw std::logic_error("not implemented"); }
  std::optional<int> get(const std::string&) { throw std::logic_error("not implemented"); }
  void put(const std::string&, int) { throw std::logic_error("not implemented"); }
  void pin(const std::string&) { throw std::logic_error("not implemented"); }
  void unpin(const std::string&) { throw std::logic_error("not implemented"); }
};
