/*
Rate Limiter, Part 1

At most capacity events in any rolling window_seconds interval. Inject a clock so tests do not sleep.

FakeClock clock;
RateLimiter lim(3, 10, [&clock] { return clock(); });
lim.allow();  // true, true, true, false

- RateLimiter(capacity, window_seconds, clock={}, max_keys=nullopt) — empty clock defaults to steady_clock. Throw std::invalid_argument if capacity < 1 or window_seconds <= 0.
- allow(key="default") -> bool — counts this call if allowed. Part 1 only needs the default key.
- Rolling window, not fixed calendar buckets.

*/
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



/*
PART 2

Per-key limits. Same window and capacity for every key.

lim.allow("a");  // true
lim.allow("a");  // true
lim.allow("a");  // false
lim.allow("b");  // true

- allow(key="default") — independent budget per key.
- No-arg allow() still works (uses "default").

*/


/*
PART 3

Per-key capacity overrides and bounded memory.

RateLimiter lim(1, 10, clock, /max_keys=/2);
lim.set_limit("vip", 5);
lim.retry_after("vip");  // seconds until next allow, 0 if allow would succeed

- max_keys=nullopt — bound distinct keys with state; nullopt unbounded. Throw if max_keys < 1.
- set_limit(key, capacity) — override capacity for key. Throw if capacity < 1.
- New key past max_keys evicts least-recently-allow()ed key (override + history gone). Configuring via set_limit does not count as a use.
- retry_after(key="default") — seconds until next allow; 0.0 if allow would succeed now. Does not count as a request.

*/
