# ABR Player — Part 2

Never underrun (“never buffer”).

The API also provides:

- `estimate_fetch_seconds(quality, index) -> float` — time to download that chunk
- `chunk_media_seconds(index) -> float` — playback duration of that chunk

`play_no_underrun() -> list[tuple[str, bytes]]`:

- Track `buffered` media seconds already downloaded ahead of the playhead.
- **Chunk 0 (startup):** may fetch at the highest quality with no underrun check;
  then `buffered = chunk_media_seconds(0)`.
- **Chunk i > 0:** pick the **highest** quality `q` such that
  `estimate_fetch_seconds(q, i) <= buffered`.
  After choosing, simulate: `buffered -= estimate`; then `buffered += media(i)`.
  (`buffered` must not go negative.)
- If even the lowest quality would underrun, raise `ValueError`.
- Return `[(quality, bytes), ...]` in chunk order.
