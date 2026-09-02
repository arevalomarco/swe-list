#include "interview_test.hpp"
#include <string>
#include "circuit_breaker.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

static void open_breaker(CircuitBreaker& cb) {
  auto boom = []() -> int { throw std::runtime_error("x"); };
  CHECK_THROWS(cb.call(boom));
  CHECK_THROWS(cb.call(boom));
}

TEST_CASE("tests/part2", "half_open_success_closes") {
  FakeClock clock;
  CircuitBreaker cb(2, 10, [&clock] { return clock(); });
  open_breaker(cb);
  bool open = false;
  try {
    cb.call([] { return 1; });
  } catch (const CircuitOpenError&) {
    open = true;
  }
  CHECK(open);
  clock.advance(10);
  CHECK(cb.call([] { return std::string("ok"); }) == "ok");
  CHECK(cb.call([] { return std::string("still"); }) == "still");
}

TEST_CASE("tests/part2", "half_open_failure_reopens") {
  FakeClock clock;
  CircuitBreaker cb(2, 10, [&clock] { return clock(); });
  open_breaker(cb);
  clock.advance(10);
  auto boom = []() -> int { throw std::runtime_error("x"); };
  CHECK_THROWS(cb.call(boom));
  bool open = false;
  try {
    cb.call([] { return 1; });
  } catch (const CircuitOpenError&) {
    open = true;
  }
  CHECK(open);
  clock.advance(9.9);
  open = false;
  try {
    cb.call([] { return 1; });
  } catch (const CircuitOpenError&) {
    open = true;
  }
  CHECK(open);
}
