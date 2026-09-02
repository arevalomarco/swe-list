#include "interview_test.hpp"
#include <string>
#include "circuit_breaker.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part1", "success_passes_through") {
  FakeClock clock;
  CircuitBreaker cb(2, 10, [&clock] { return clock(); });
  CHECK(cb.call([] { return 42; }) == 42);
}

TEST_CASE("tests/part1", "opens_after_threshold") {
  FakeClock clock;
  CircuitBreaker cb(2, 10, [&clock] { return clock(); });
  auto boom = []() -> int { throw std::runtime_error("x"); };
  CHECK_THROWS(cb.call(boom));
  CHECK_THROWS(cb.call(boom));
  bool open = false;
  try {
    cb.call([] { return 1; });
  } catch (const CircuitOpenError&) {
    open = true;
  }
  CHECK(open);
}

TEST_CASE("tests/part1", "success_resets_consecutive") {
  FakeClock clock;
  CircuitBreaker cb(2, 10, [&clock] { return clock(); });
  auto boom = []() -> std::string { throw std::runtime_error("x"); };
  CHECK_THROWS(cb.call(boom));
  CHECK(cb.call([] { return std::string("ok"); }) == "ok");
  CHECK_THROWS(cb.call(boom));
  CHECK(cb.call([] { return std::string("ok2"); }) == "ok2");
}
