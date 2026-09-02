"""
Arithmetic Encode, Part 1

Encode a lowercase string as a number in [0, 1) by splitting ranges.

Alphabet a..z (26 letters). Start with [low, high) = [0.0, 1.0).

For each character c in the message:

- Split [low, high) into 26 equal chunks of width (high - low) / 26.
- Chunk 0 → 'a', …, chunk 25 → 'z'.
- Narrow to the chunk for c.

encode(message) -> float — any value in the final interval (use the midpoint).

decode(x, length) -> str — recover the string of the given length.

Non a..z → ValueError. Empty message → 0.0 / "".

encode("ab")  # in [1/262, 2/262)
decode(encode("ab"), 2) == "ab"

"""
def encode(message: str) -> float:
    raise NotImplementedError


def decode(x: float, length: int) -> str:
    raise NotImplementedError




"""
PART 2

Non-uniform chunks from character frequencies.

encode(message, frequencies) / decode(x, length, frequencies):

- frequencies: dict[str, int] letter → positive weight.
- Partition [low, high) into subintervals with widths proportional to
  weight / total, letters in sorted key order.
- Narrow to the letter’s subinterval (classic arithmetic coding).
- Missing letter in frequencies, non-positive weight, or empty frequencies
  while encoding a non-empty message → ValueError.

freq = {"a": 3, "b": 2, "c": 1}
decode(encode("ab", freq), 2, freq) == "ab"

Uniform a..z from part 1 remains available as encode(message) /
decode(x, length) (no frequencies arg).

"""


"""
PART 3

Adaptive model — no fixed frequency table.

encode_adaptive(message) -> float / decode_adaptive(x, length) -> str:

- Alphabet a..z. Start every letter’s count at 1 (Laplace).
- For each symbol, partition using current counts (sorted letter order),
  narrow, then increment that letter’s count by 1.
- Encoder and decoder must apply the same updates in the same order.
- Round-trip: decode_adaptive(encode_adaptive(s), len(s)) == s.
- Non a..z → ValueError.

"""
