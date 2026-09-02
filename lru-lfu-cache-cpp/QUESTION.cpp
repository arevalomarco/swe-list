/*
LRU / LFU Cache, Part 1

LRUCache(capacity): fixed-size string-to-int cache. capacity is a positive integer.
Throw std::invalid_argument otherwise.

- get(key) returns optional<int> — nullopt if absent. A hit counts as a use.
- put(key, value) inserts or updates. Updating an existing key counts as a use.
- A brand-new key that would push the cache past capacity evicts the least recently used entry first.

LRUCache cache(2);
cache.put("a", 1);
cache.put("b", 2);
cache.get("a");  // 1
cache.put("c", 3);
cache.get("b");  // nullopt

*/
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



/*
PART 2

Some entries must not be evicted.

- pin(key) / unpin(key)
- pin / unpin on a key not in the cache throw std::invalid_argument.
- A put that would insert a new key while every entry is pinned throws std::invalid_argument.

*/


/*
PART 3

Make eviction pluggable. Pinned keys stay outside the policy.

- Cache(capacity, policy=nullptr). policy=nullptr defaults to LRU among evictable keys.
  The caller owns policy when passing one in.
- LRUPolicy and LFUPolicy. LFU ties break by LRU among the tied keys.
- set_policy(new_policy) reseeds from the old policy's eviction order — most evictable first, evictable keys only.
- LRUCache from parts 1–2 keeps working from the outside.

LRUPolicy lru;
Cache cache(2, &lru);
cache.set_policy(&lfu);  // next eviction unchanged by the swap itself

*/
