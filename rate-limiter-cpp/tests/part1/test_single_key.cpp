#include "interview_test.hpp"
#include "rate_limiter.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part1", "allows_up_to_capacity_then_denies") {
  FakeClock clock;
  RateLimiter limiter(3, 10, [&clock] { return clock(); });
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == false);
}

TEST_CASE("tests/part1", "capacity_frees_up_as_the_window_slides") {
  FakeClock clock;
  RateLimiter limiter(2, 10, [&clock] { return clock(); });
  CHECK(limiter.allow() == true);
  clock.advance(5);
  CHECK(limiter.allow() == true);
  clock.advance(5.5);
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == false);
}

TEST_CASE("tests/part1", "a_fully_elapsed_window_resets_capacity") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == false);
  clock.advance(10.1);
  CHECK(limiter.allow() == true);
}

TEST_CASE("tests/part1", "fixed_reset_boundary_would_wrongly_allow_double_capacity") {
  FakeClock clock;
  RateLimiter limiter(2, 10, [&clock] { return clock(); });
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == true);
  clock.advance(9.9);
  CHECK(limiter.allow() == false);
}

TEST_CASE("tests/part1", "non_positive_capacity_is_rejected") {
  CHECK_THROWS(RateLimiter(0, 10));
  CHECK_THROWS(RateLimiter(-1, 10));
}

TEST_CASE("tests/part1", "non_positive_window_is_rejected") {
  CHECK_THROWS(RateLimiter(1, 0));
  CHECK_THROWS(RateLimiter(1, -5));
}
