import random

import pytest

from solution.diff_merge import apply, diff


def test_round_trip_on_empty_lists():
    assert apply([], diff([], [])) == []


def test_round_trip_on_identical_nonempty_lists():
    lines = ["alpha", "beta", "gamma"]
    assert apply(lines, diff(lines, list(lines))) == lines


def test_round_trip_on_disjoint_lists():
    old = ["a", "b"]
    new = ["x", "y"]
    assert apply(old, diff(old, new)) == new


def test_round_trip_on_a_middle_replacement():
    old = ["a", "b", "c", "d"]
    new = ["a", "x", "y", "d"]
    assert apply(old, diff(old, new)) == new


def test_apply_rejects_a_patch_that_does_not_match():
    old = ["1", "2", "3"]
    patch = diff(["9", "9", "9"], ["1", "2", "3"])
    with pytest.raises(ValueError):
        apply(old, patch)


def test_apply_round_trip_on_random_small_inputs():
    rng = random.Random(20260819)
    alphabet = ["a", "b", "c", "d", "e", ""]
    for _ in range(200):
        old = [rng.choice(alphabet) for _ in range(rng.randint(0, 8))]
        new = [rng.choice(alphabet) for _ in range(rng.randint(0, 8))]
        assert apply(old, diff(old, new)) == new, (old, new)
