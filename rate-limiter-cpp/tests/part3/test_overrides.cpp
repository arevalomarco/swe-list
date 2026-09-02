#include "interview_test.hpp"
#include "rate_limiter.hpp"

struct FakeClock {
  double t = 0;
  double operator()() const { return t; }
  void advance(double dt) { t += dt; }
};

TEST_CASE("tests/part3", "set_limit_overrides_capacity_for_that_key_only") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  limiter.set_limit("vip", 3);
  CHECK(limiter.allow("vip") == true);
  CHECK(limiter.allow("vip") == true);
  CHECK(limiter.allow("vip") == true);
  CHECK(limiter.allow("vip") == false);
  CHECK(limiter.allow("normal") == true);
  CHECK(limiter.allow("normal") == false);
}

TEST_CASE("tests/part3", "set_limit_rejects_non_positive_capacity") {
  RateLimiter limiter(1, 10);
  CHECK_THROWS(limiter.set_limit("vip", 0));
}

TEST_CASE("tests/part3", "retry_after_reports_time_remaining") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  CHECK_NEAR(limiter.retry_after(), 0.0, 1e-9);
  limiter.allow();
  CHECK_NEAR(limiter.retry_after(), 10.0, 1e-9);
  clock.advance(4);
  CHECK_NEAR(limiter.retry_after(), 6.0, 1e-9);
  clock.advance(6);
  CHECK_NEAR(limiter.retry_after(), 0.0, 1e-9);
}

TEST_CASE("tests/part3", "retry_after_does_not_consume_budget") {
  FakeClock clock;
  RateLimiter limiter(1, 10, [&clock] { return clock(); });
  limiter.allow();
  for (int i = 0; i < 5; ++i) limiter.retry_after();
  clock.advance(10.1);
  CHECK(limiter.allow() == true);
}

TEST_CASE("tests/part3", "max_keys_evicts_lru_key") {
  FakeClock clock;
  RateLimiter limiter(1, 100, [&clock] { return clock(); }, 2);
  limiter.set_limit("a", 5);
  clock.advance(1);
  CHECK(limiter.allow("b") == true);
  clock.advance(1);
  CHECK(limiter.allow("c") == true);
  CHECK(limiter.allow("a") == true);
  CHECK(limiter.allow("a") == false);
}

TEST_CASE("tests/part3", "unbounded_by_default_never_evicts") {
  FakeClock clock;
  RateLimiter limiter(1, 100, [&clock] { return clock(); });
  for (int i = 0; i < 50; ++i) {
    clock.advance(1);
    CHECK(limiter.allow("key-" + std::to_string(i)) == true);
  }
  CHECK(limiter.allow("key-0") == false);
  CHECK(limiter.allow("key-49") == false);
}

TEST_CASE("tests/part3", "max_keys_must_be_at_least_one_or_none") {
  CHECK_THROWS(RateLimiter(1, 10, {}, 0));
  CHECK_THROWS(RateLimiter(1, 10, {}, -1));
}
