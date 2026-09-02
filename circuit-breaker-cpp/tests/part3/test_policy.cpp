#include "interview_test.hpp"
#include <string>
#include "circuit_breaker.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part3", "error_rate_policy") {
  FakeClock clock;
  ErrorRatePolicy policy(10, 0.6);
  CircuitBreaker cb(99, 10, [&clock] { return clock(); }, &policy);
  auto boom = []() -> int { throw std::runtime_error("x"); };
  CHECK(cb.call([] { return 1; }) == 1);
  clock.advance(1);
  CHECK_THROWS(cb.call(boom));
  clock.advance(1);
  CHECK_THROWS(cb.call(boom));
  bool open = false;
  try {
    cb.call([] { return 1; });
  } catch (const CircuitOpenError&) {
    open = true;
  }
  CHECK(open);
}

TEST_CASE("tests/part3", "set_policy_resets") {
  FakeClock clock;
  CircuitBreaker cb(2, 10, [&clock] { return clock(); });
  auto boom = []() -> int { throw std::runtime_error("x"); };
  CHECK_THROWS(cb.call(boom));
  ConsecutiveFailures next(2);
  cb.set_policy(&next);
  CHECK_THROWS(cb.call(boom));
  CHECK(cb.call([] { return std::string("ok"); }) == "ok");
}
