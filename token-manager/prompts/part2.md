# Token Manager — Part 2

`count_unexpired` should not be O(all tokens) every time if you can avoid it.

## Requirements

- Keep an expiry-ordered structure and lazy-evict on generate/renew/count
- Same external API as part 1
