cmake_minimum_required(VERSION 3.16)
project(interview LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

file(GLOB_RECURSE TEST_SOURCES CONFIGURE_DEPENDS "${CMAKE_SOURCE_DIR}/tests/*.cpp")
list(APPEND TEST_SOURCES "${CMAKE_SOURCE_DIR}/test_main.cpp")

add_executable(interview_tests ${TEST_SOURCES})
target_include_directories(interview_tests PRIVATE
  "${CMAKE_SOURCE_DIR}/solution"
  "${CMAKE_SOURCE_DIR}/third_party")
if(DEFINED INTERVIEW_TEST_INCLUDE AND NOT "${INTERVIEW_TEST_INCLUDE}" STREQUAL "")
  target_include_directories(interview_tests PRIVATE "${INTERVIEW_TEST_INCLUDE}")
endif()
