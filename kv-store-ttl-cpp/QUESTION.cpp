/*
KV Store + TTL, Part 1

KVStore kv;
kv.put("a", 1);
kv.get("a");     // 1
kv.erase("a");   // true  (erase, not delete — delete is a keyword)
kv.get("a");     // nullopt

- KVStore()
- put(key, value) — values are int
- get(key) -> optional<int>
- erase(key) -> bool

*/
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



/*
PART 2

KVStore kv(clock);
kv.put("a", 1, /ttl=/10);
// after 10s...
kv.get("a");  // nullopt — entry dropped lazily

- KVStore(clock={}) — empty clock defaults to 0 (tests inject one)
- put(key, value, ttl=nullopt) — ttl seconds from now; nullopt means forever
- get on expired key returns nullopt and drops the entry
- put without ttl on an existing key clears ttl

*/


/*
PART 3

Watchers. unwatch(key) removes all callbacks for that key.

kv.watch("a", cb);
kv.put("a", 2);      // cb("a", 2)
kv.erase("a");       // cb("a", nullopt)
kv.expire_due();     // notifies watchers for newly discovered expiries

- watch(key, callback) / unwatch(key)
- callback(key, new_value_or_nullopt) on put/erase/expiry
- Expiry must notify when discovered via get or expire_due()

*/
