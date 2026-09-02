# ABR Player — Part 1

Stream media chunks using **their** API, at the highest quality.

Provided API (injected; do not reimplement the fake — duck-type whatever is passed in):

- `qualities() -> list[str]` — ordered low → high (e.g. `["360p", "720p", "1080p"]`)
- `num_chunks() -> int`
- `fetch(quality, index) -> bytes`

`Player(api)`:

- `play_max_quality() -> list[bytes]`
  Fetch chunks `0 .. n-1` in order at the **highest** quality. Return the bytes list.

```python
player = Player(api)
player.play_max_quality()  # [chunk0, chunk1, ...]
```
