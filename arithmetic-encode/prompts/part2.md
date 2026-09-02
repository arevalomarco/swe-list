# Arithmetic Encode — Part 2

Non-uniform chunks from character frequencies.

`encode(message, frequencies)` / `decode(x, length, frequencies)`:

- `frequencies`: `dict[str, int]` letter → positive weight.
- Partition `[low, high)` into subintervals with widths proportional to
  `weight / total`, letters in **sorted** key order.
- Narrow to the letter’s subinterval (classic arithmetic coding).
- Missing letter in `frequencies`, non-positive weight, or empty frequencies
  while encoding a non-empty message → `ValueError`.

```python
freq = {"a": 3, "b": 2, "c": 1}
decode(encode("ab", freq), 2, freq) == "ab"
```

Uniform `a..z` from part 1 remains available as `encode(message)` /
`decode(x, length)` (no frequencies arg).
