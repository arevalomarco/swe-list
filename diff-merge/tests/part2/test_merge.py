from solution.diff_merge import merge


def test_merge_returns_base_when_neither_side_changed():
    base = ["1", "2", "3"]
    assert merge(base, list(base), list(base)) == base


def test_merge_takes_one_side_when_the_other_is_unchanged():
    base = ["1", "2", "3"]
    mine = ["1", "X", "3"]
    theirs = ["1", "Y", "Z", "3"]
    assert merge(base, mine, list(base)) == mine
    assert merge(base, list(base), theirs) == theirs


def test_merge_combines_independent_edits():
    base = ["1", "2", "3", "4", "5"]
    mine = ["1", "X", "3", "4", "5"]
    theirs = ["1", "2", "3", "4", "Z"]
    assert merge(base, mine, theirs) == ["1", "X", "3", "4", "Z"]


def test_merge_applies_an_identical_change_once():
    base = ["1", "2", "3"]
    both = ["1", "X", "3"]
    assert merge(base, both, list(both)) == both


def test_unrelated_insertions_at_different_gaps_combine():
    base = ["1", "2", "3"]
    mine = ["0", "1", "2", "3"]
    theirs = ["1", "2", "3", "4"]
    assert merge(base, mine, theirs) == ["0", "1", "2", "3", "4"]


def test_one_side_deleting_while_the_other_leaves_the_line_alone_drops_it():
    base = ["1", "2", "3"]
    mine = ["1", "3"]
    assert merge(base, mine, list(base)) == ["1", "3"]


def test_both_sides_deleting_the_same_line_is_not_a_conflict():
    base = ["1", "2", "3"]
    both = ["1", "3"]
    assert merge(base, both, list(both)) == ["1", "3"]


def test_a_pure_insertion_by_only_one_side_is_never_a_conflict():
    base = ["1", "2", "3"]
    mine = ["1", "A", "2", "3"]
    assert merge(base, mine, list(base)) == ["1", "A", "2", "3"]
