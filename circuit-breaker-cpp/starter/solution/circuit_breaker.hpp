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
