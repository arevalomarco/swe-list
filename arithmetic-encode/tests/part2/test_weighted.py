import pytest

from solution.codec import decode, encode


def test_weighted_round_trip():
    freq = {"a": 3, "b": 2, "c": 1}
    for s in ["a", "b", "c", "ab", "bac", "aaa"]:
        assert decode(encode(s, freq), len(s), freq) == s


def test_uniform_still_works_without_freq():
    assert decode(encode("xyz"), 3) == "xyz"


def test_missing_letter_raises():
    freq = {"a": 1, "b": 1}
    with pytest.raises(ValueError):
        encode("c", freq)


def test_non_positive_weight_raises():
    with pytest.raises(ValueError):
        encode("a", {"a": 0})
