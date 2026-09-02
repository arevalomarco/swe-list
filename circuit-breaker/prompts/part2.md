# Circuit Breaker — Part 2

Half-open after cool_down.

## Requirements

- Once open, after `cool_down_seconds` a single trial call is allowed (half-open)
- Success -> closed. Failure -> open again and reset cool_down timer
