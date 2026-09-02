import pytest

from solution.codec import decode, encode


def test_round_trip_short():
    for s in ["a", "ab", "z", "hello", "python"]:
        assert decode(encode(s), len(s)) == s


def test_empty():
    assert encode("") == 0.0
    assert decode(0.0, 0) == ""


def test_encode_ab_in_expected_interval():
    x = encode("ab")
    # after a: [0, 1/26); after b: [1/26^2, 2/26^2)
    lo, hi = 1 / 26**2, 2 / 26**2
    assert lo <= x < hi


def test_rejects_non_lowercase():
    with pytest.raises(ValueError):
        encode("A")
    with pytest.raises(ValueError):
        encode("a1")
