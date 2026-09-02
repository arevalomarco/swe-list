"""
ABR Player, Part 1

Stream media chunks using their API, at the highest quality.

Provided API (injected; do not reimplement the fake — duck-type whatever is passed in):

- qualities() -> list[str] — ordered low → high (e.g. ["360p", "720p", "1080p"])
- num_chunks() -> int
- fetch(quality, index) -> bytes

Player(api):

- play_max_quality() -> list[bytes]
  Fetch chunks 0 .. n-1 in order at the highest quality. Return the bytes list.

player = Player(api)
player.play_max_quality()  # [chunk0, chunk1, ...]

"""
class Player:
    def __init__(self, api):
        raise NotImplementedError

    def play_max_quality(self):
        raise NotImplementedError




"""
PART 2

Never underrun (“never buffer”).

The API also provides:

- estimate_fetch_seconds(quality, index) -> float — time to download that chunk
- chunk_media_seconds(index) -> float — playback duration of that chunk

play_no_underrun() -> list[tuple[str, bytes]]:

- Track buffered media seconds already downloaded ahead of the playhead.
- Chunk 0 (startup): may fetch at the highest quality with no underrun check;
  then buffered = chunk_media_seconds(0).
- Chunk i > 0: pick the highest quality q such that
  estimate_fetch_seconds(q, i) <= buffered.
  After choosing, simulate: buffered -= estimate; then buffered += media(i).
  (buffered must not go negative.)
- If even the lowest quality would underrun, raise ValueError.
- Return [(quality, bytes), ...] in chunk order.

"""


"""
PART 3

Smooth quality changes.

Same underrun rules as part 2, plus:

- play_smooth(max_step=1) -> list[tuple[str, bytes]]
- Quality index may change by at most max_step rungs per chunk
  (up or down) relative to the quality used for the previous chunk.
- Among legal qualities that also satisfy the underrun constraint, pick the
  highest.
- Chunk 0: still highest quality (startup), ignoring max_step.
- Underrun with no legal quality → ValueError.

"""
