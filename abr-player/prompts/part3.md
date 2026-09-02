# ABR Player — Part 3

Smooth quality changes.

Same underrun rules as part 2, plus:

- `play_smooth(max_step=1) -> list[tuple[str, bytes]]`
- Quality index may change by at most `max_step` rungs per chunk
  (up or down) relative to the quality used for the previous chunk.
- Among legal qualities that also satisfy the underrun constraint, pick the
  **highest**.
- Chunk 0: still highest quality (startup), ignoring `max_step`.
- Underrun with no legal quality → `ValueError`.
