# Arithmetic Encode — Part 3

Adaptive model — no fixed frequency table.

`encode_adaptive(message) -> float` / `decode_adaptive(x, length) -> str`:

- Alphabet `a..z`. Start every letter’s count at **1** (Laplace).
- For each symbol, partition using **current** counts (sorted letter order),
  narrow, then **increment** that letter’s count by 1.
- Encoder and decoder must apply the same updates in the same order.
- Round-trip: `decode_adaptive(encode_adaptive(s), len(s)) == s`.
- Non `a..z` → `ValueError`.
