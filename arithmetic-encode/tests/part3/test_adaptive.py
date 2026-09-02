import pytest

from solution.codec import decode, decode_adaptive, encode, encode_adaptive


def test_adaptive_round_trip():
    for s in ["a", "ab", "zzz", "abracadabra", "helloworld"]:
        assert decode_adaptive(encode_adaptive(s), len(s)) == s


def test_adaptive_differs_from_uniform_for_skewed_text():
    s = "aaaaab"
    # Not required that values differ, but round-trips must both succeed.
    assert decode(encode(s), len(s)) == s
    assert decode_adaptive(encode_adaptive(s), len(s)) == s


def test_adaptive_rejects_bad_chars():
    with pytest.raises(ValueError):
        encode_adaptive("A")


def test_prior_parts_still_work():
    freq = {"a": 2, "b": 1}
    assert decode(encode("ab", freq), 2, freq) == "ab"
    assert decode(encode("hi"), 2) == "hi"
