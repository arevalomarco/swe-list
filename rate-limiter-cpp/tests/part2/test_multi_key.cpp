#include "interview_test.hpp"
#include "rate_limiter.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part2", "allow_with_no_key_behaves_like_part_1") {
  FakeClock clock;
  RateLimiter limiter(2, 10, [&clock] { return clock(); });
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == true);
  CHECK(limiter.allow() == false);
}

TEST_CASE("tests/part2", "different_keys_have_fully_independent_budgets") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  CHECK(limiter.allow("alice") == true);
  CHECK(limiter.allow("bob") == true);
  CHECK(limiter.allow("alice") == false);
  CHECK(limiter.allow("bob") == false);
}

TEST_CASE("tests/part2", "the_same_key_shares_its_budget") {
  FakeClock clock;
  RateLimiter limiter(2, 10, [&clock] { return clock(); });
  CHECK(limiter.allow("x") == true);
  CHECK(limiter.allow("x") == true);
  CHECK(limiter.allow("x") == false);
}

TEST_CASE("tests/part2", "never_before_seen_key_starts_full") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  limiter.allow("a");
  CHECK(limiter.allow("z") == true);
}

TEST_CASE("tests/part2", "each_key_slides_its_own_window") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  CHECK(limiter.allow("a") == true);
  clock.advance(5);
  CHECK(limiter.allow("b") == true);
  clock.advance(5.1);
  CHECK(limiter.allow("a") == true);
  CHECK(limiter.allow("b") == false);
}
