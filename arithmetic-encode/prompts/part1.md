# Arithmetic Encode — Part 1

Encode a lowercase string as a number in `[0, 1)` by splitting ranges.

Alphabet `a..z` (26 letters). Start with `[low, high) = [0.0, 1.0)`.

For each character `c` in the message:

- Split `[low, high)` into 26 equal chunks of width `(high - low) / 26`.
- Chunk 0 → `'a'`, …, chunk 25 → `'z'`.
- Narrow to the chunk for `c`.

`encode(message) -> float` — any value in the final interval (use the midpoint).

`decode(x, length) -> str` — recover the string of the given length.

Non `a..z` → `ValueError`. Empty message → `0.0` / `""`.

```python
encode("ab")  # in [1/26**2, 2/26**2)
decode(encode("ab"), 2) == "ab"
```
