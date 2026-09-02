#pragma once

/**
 * Minimal JUnit-emitting test harness for C++ interview questions.
 *
 * One TEST_CASE per test, first argument the suite directory (must match the
 * question's testDir, e.g. "tests/part1") so part attribution is data, not a regex.
 * Define INTERVIEW_TEST_MAIN in exactly one translation unit (starter/test_main.cpp).
 */

#include <chrono>
#include <cmath>
#include <cstdlib>
#include <exception>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

struct InterviewAssertion : std::exception {
  std::string message;
  const char* file;
  int line;
  InterviewAssertion(std::string message, const char* file, int line)
      : message(std::move(message)), file(file), line(line) {}
  const char* what() const noexcept override { return message.c_str(); }
};

struct InterviewTest {
  const char* suite;
  const char* name;
  void (*fn)();
};

inline std::vector<InterviewTest>& interview_registry() {
  static std::vector<InterviewTest> tests;
  return tests;
}

struct InterviewRegistrar {
  InterviewRegistrar(const char* suite, const char* name, void (*fn)()) {
    interview_registry().push_back({suite, name, fn});
  }
};

#define INTERVIEW_CONCAT_(a, b) a##b
#define INTERVIEW_CONCAT(a, b) INTERVIEW_CONCAT_(a, b)

#define TEST_CASE(suite, name)                                                                         \
  static void INTERVIEW_CONCAT(interview_fn_, __LINE__)();                                             \
  static InterviewRegistrar INTERVIEW_CONCAT(interview_reg_, __LINE__)(                                \
      suite, name, &INTERVIEW_CONCAT(interview_fn_, __LINE__));                                        \
  static void INTERVIEW_CONCAT(interview_fn_, __LINE__)()

#define CHECK(expr)                                                                                    \
  do {                                                                                                 \
    if (!(expr)) {                                                                                     \
      throw InterviewAssertion("CHECK(" #expr ") failed", __FILE__, __LINE__);                         \
    }                                                                                                  \
  } while (0)

#define CHECK_EQ(a, b)                                                                                 \
  do {                                                                                                 \
    const auto interview_av = (a);                                                                     \
    const auto interview_bv = (b);                                                                     \
    if (!(interview_av == interview_bv)) {                                                             \
      std::ostringstream interview_os;                                                                 \
      interview_os << "CHECK_EQ(" #a ", " #b ") failed";                                               \
      throw InterviewAssertion(interview_os.str(), __FILE__, __LINE__);                                \
    }                                                                                                  \
  } while (0)

#define CHECK_NE(a, b)                                                                                 \
  do {                                                                                                 \
    const auto interview_av = (a);                                                                     \
    const auto interview_bv = (b);                                                                     \
    if (interview_av == interview_bv) {                                                                \
      throw InterviewAssertion("CHECK_NE(" #a ", " #b ") failed", __FILE__, __LINE__);                 \
    }                                                                                                  \
  } while (0)

#define CHECK_NEAR(a, b, eps)                                                                          \
  do {                                                                                                 \
    const double interview_av = static_cast<double>(a);                                                \
    const double interview_bv = static_cast<double>(b);                                                \
    if (std::fabs(interview_av - interview_bv) > (eps)) {                                              \
      std::ostringstream interview_os;                                                                 \
      interview_os << "CHECK_NEAR(" #a ", " #b ") failed: " << interview_av << " vs " << interview_bv;  \
      throw InterviewAssertion(interview_os.str(), __FILE__, __LINE__);                                \
    }                                                                                                  \
  } while (0)

#define CHECK_THROWS(expr)                                                                             \
  do {                                                                                                 \
    bool interview_threw = false;                                                                      \
    try {                                                                                              \
      (void)(expr);                                                                                    \
    } catch (...) {                                                                                    \
      interview_threw = true;                                                                          \
    }                                                                                                  \
    if (!interview_threw) {                                                                            \
      throw InterviewAssertion("CHECK_THROWS(" #expr ") did not throw", __FILE__, __LINE__);           \
    }                                                                                                  \
  } while (0)

#ifdef INTERVIEW_TEST_MAIN

inline std::string interview_xml_escape(const std::string& text) {
  std::string out;
  out.reserve(text.size());
  for (char c : text) {
    switch (c) {
      case '&':
        out += "&amp;";
        break;
      case '<':
        out += "&lt;";
        break;
      case '>':
        out += "&gt;";
        break;
      case '"':
        out += "&quot;";
        break;
      case '\'':
        out += "&apos;";
        break;
      default:
        out += c;
        break;
    }
  }
  return out;
}

int main(int argc, char** argv) {
  std::string junit_path;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    const std::string prefix = "--junit-xml=";
    if (arg.rfind(prefix, 0) == 0) junit_path = arg.substr(prefix.size());
  }

  struct Result {
    const char* suite;
    const char* name;
    bool passed;
    bool errored;
    std::string message;
    double seconds;
  };
  std::vector<Result> results;
  int failed = 0;
  int errored = 0;

  for (const InterviewTest& test : interview_registry()) {
    const auto started = std::chrono::steady_clock::now();
    Result result{test.suite, test.name, true, false, "", 0.0};
    try {
      test.fn();
    } catch (const InterviewAssertion& assertion) {
      result.passed = false;
      result.message = assertion.message + " (" + assertion.file + ":" + std::to_string(assertion.line) + ")";
      ++failed;
    } catch (const std::exception& ex) {
      result.passed = false;
      result.errored = true;
      result.message = ex.what();
      ++errored;
    } catch (...) {
      result.passed = false;
      result.errored = true;
      result.message = "unknown exception";
      ++errored;
    }
    result.seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    results.push_back(result);
    if (!result.passed) {
      std::cerr << "FAILED " << test.suite << "::" << test.name << " — " << result.message << "\n";
    }
  }

  if (!junit_path.empty()) {
    std::ofstream out(junit_path.c_str());
    const int total = static_cast<int>(results.size());
    out << "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    out << "<testsuite name=\"interview_tests\" tests=\"" << total << "\" failures=\"" << failed
        << "\" errors=\"" << errored << "\" skipped=\"0\">\n";
    for (const Result& result : results) {
      out << "  <testcase classname=\"" << interview_xml_escape(result.suite) << "\" name=\""
          << interview_xml_escape(result.name) << "\" time=\"" << result.seconds << "\"";
      if (result.passed) {
        out << "/>\n";
      } else if (result.errored) {
        out << ">\n    <error message=\"" << interview_xml_escape(result.message) << "\"/>\n  </testcase>\n";
      } else {
        out << ">\n    <failure message=\"" << interview_xml_escape(result.message) << "\"/>\n  </testcase>\n";
      }
    }
    out << "</testsuite>\n";
  }

  std::cout << (results.size() - static_cast<size_t>(failed) - static_cast<size_t>(errored)) << "/"
            << results.size() << " passed\n";
  return failed + errored == 0 ? 0 : 1;
}

#endif
