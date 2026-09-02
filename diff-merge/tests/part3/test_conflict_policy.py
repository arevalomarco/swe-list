import pytest

from solution.diff_merge import Markers, PreferMine, PreferTheirs, RaiseOnConflict, merge


def test_default_policy_raises_on_conflicting_edits_to_the_same_line():
    base = ["1", "2", "3"]
    with pytest.raises(ValueError):
        merge(base, ["1", "X", "3"], ["1", "Y", "3"])


def test_default_policy_raises_on_conflicting_insertions_at_the_same_gap():
    base = ["1", "2", "3"]
    with pytest.raises(ValueError):
        merge(base, ["1", "A", "2", "3"], ["1", "B", "2", "3"])


def test_default_policy_fails_the_whole_merge_on_any_conflict():
    base = ["1", "2", "3", "4", "5"]
    with pytest.raises(ValueError):
        merge(base, ["1", "X", "3", "4", "W"], ["1", "2", "3", "4", "Z"])


def test_raise_on_conflict_policy_raises_explicitly():
    base = ["1", "2", "3"]
    with pytest.raises(ValueError):
        merge(base, ["1", "X", "3"], ["1", "Y", "3"], policy=RaiseOnConflict())


def test_prefer_mine_keeps_mine_on_a_line_edit_conflict():
    base = ["1", "2", "3"]
    assert merge(base, ["1", "X", "3"], ["1", "Y", "3"], policy=PreferMine()) == ["1", "X", "3"]


def test_prefer_theirs_keeps_theirs_on_a_line_edit_conflict():
    base = ["1", "2", "3"]
    assert merge(base, ["1", "X", "3"], ["1", "Y", "3"], policy=PreferTheirs()) == ["1", "Y", "3"]


def test_prefer_mine_is_what_part_2_silently_did_for_overlapping_gaps():
    base = ["1", "2", "3"]
    assert merge(base, ["1", "A", "2", "3"], ["1", "B", "2", "3"], policy=PreferMine()) == [
        "1",
        "A",
        "2",
        "3",
    ]


def test_markers_wraps_a_gap_conflict_with_both_sides():
    base = ["1", "2"]
    assert merge(base, ["1", "A", "2"], ["1", "B", "2"], policy=Markers()) == [
        "1",
        "<<<<<<< mine",
        "A",
        "=======",
        "B",
        ">>>>>>> theirs",
        "2",
    ]


def test_identical_edits_to_the_same_line_are_still_not_a_conflict():
    base = ["1", "2", "3"]
    both = ["1", "X", "3"]
    assert merge(base, both, list(both)) == both
    assert merge(base, both, list(both), policy=RaiseOnConflict()) == both


def test_one_side_deleting_and_the_other_leaving_it_unchanged_is_not_a_conflict():
    base = ["1", "2", "3"]
    assert merge(base, ["1", "3"], list(base)) == ["1", "3"]
    assert merge(base, ["1", "3"], list(base), policy=RaiseOnConflict()) == ["1", "3"]
