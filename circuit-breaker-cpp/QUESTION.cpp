/*
Circuit Breaker, Part 1

CircuitBreaker cb(2, 10, clock);
cb.call(ok_fn);     // returns result
cb.call(bad_fn);    // throws original; counts failure
// after threshold consecutive failures, further call throws CircuitOpenError without invoking fn

- CircuitBreaker(failure_threshold, cool_down_seconds, clock={}, policy=nullptr)
- call(fn) — fn is any nullary callable
- Exception from fn counts a failure; success resets consecutive failure count
- After failure_threshold consecutive failures, state is open: call throws CircuitOpenError

*/
#pragma once

#include <functional>
#include <stdexcept>
#include <utility>

class CircuitOpenError : public std::runtime_error {
 public:
  CircuitOpenError() : std::runtime_error("circuit open") {}
};

class TripPolicy {
 public:
  virtual ~TripPolicy() = default;
  virtual void reset() = 0;
  virtual bool on_success(double now) = 0;
  virtual bool on_failure(double now) = 0;
};

class ConsecutiveFailures : public TripPolicy {
 public:
  explicit ConsecutiveFailures(int threshold) { (void)threshold; }
  void reset() override {}
  bool on_success(double) override { return false; }
  bool on_failure(double) override { throw std::logic_error("not implemented"); }
};

class ErrorRatePolicy : public TripPolicy {
 public:
  ErrorRatePolicy(double window, double rate) {
    (void)window;
    (void)rate;
  }
  void reset() override {}
  bool on_success(double) override { return false; }
  bool on_failure(double) override { throw std::logic_error("not implemented"); }
};

class CircuitBreaker {
 public:
  CircuitBreaker(int failure_threshold, double cool_down_seconds, std::function<double()> clock = {},
                 TripPolicy* policy = nullptr) {
    (void)failure_threshold;
    (void)cool_down_seconds;
    (void)clock;
    (void)policy;
    throw std::logic_error("not implemented");
  }

  template <typename F>
  auto call(F fn) -> decltype(fn()) {
    throw std::logic_error("not implemented");
    return fn();
  }

  void set_policy(TripPolicy* policy) {
    (void)policy;
    throw std::logic_error("not implemented");
  }
};



/*
PART 2

Half-open after cool_down.

- Once open, after cool_down_seconds a single trial call is allowed (half-open)
- Success -> closed. Failure -> open again and reset cool_down timer

*/


/*
PART 3

Pluggable trip policy. The caller owns policy when passing one in.

ConsecutiveFailures consec(2);
ErrorRatePolicy rate(/window=/5, /rate=/0.5);
CircuitBreaker cb(2, 10, clock, &consec);
cb.set_policy(&rate);

- Default policy: consecutive failures (same as parts 1–2)
- ErrorRatePolicy(window, rate) — open when failures/attempts in the last window seconds >= rate
- set_policy swaps; counters / windows reset; if currently open, cool_down restarts from now

*/
