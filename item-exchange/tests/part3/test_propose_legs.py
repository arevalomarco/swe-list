import pytest

from solution.item_exchange import Exchange


def test_propose_legs_three_way_and_accept():
    ex = Exchange()
    ex.set_inventory("a", "x", 1)
    ex.set_inventory("b", "y", 1)
    ex.set_inventory("c", "z", 1)
    tid = ex.propose_legs(
        [
            ("a", "b", "x", 1),
            ("b", "c", "y", 1),
            ("c", "a", "z", 1),
        ]
    )
    assert ex.get("a", "x") == 0
    assert ex.get("b", "y") == 0
    assert ex.get("c", "z") == 0
    ex.accept(tid)
    assert ex.get("a", "z") == 1
    assert ex.get("b", "x") == 1
    assert ex.get("c", "y") == 1
    assert ex.get("a", "x") == 0


def test_propose_legs_rolls_back_if_any_leg_fails():
    ex = Exchange()
    ex.set_inventory("a", "x", 1)
    ex.set_inventory("b", "y", 0)
    with pytest.raises(ValueError):
        ex.propose_legs(
            [
                ("a", "b", "x", 1),
                ("b", "a", "y", 1),
            ]
        )
    assert ex.get("a", "x") == 1
    assert ex.get("b", "y") == 0


def test_propose_still_works_as_two_leg_swap():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 2)
    ex.set_inventory("bob", "coin", 5)
    tid = ex.propose("alice", "bob", "apple", 1, "coin", 2)
    ex.accept(tid)
    assert ex.get("alice", "coin") == 2
    assert ex.get("bob", "apple") == 1


def test_cancel_multi_leg_releases_all():
    ex = Exchange()
    ex.set_inventory("a", "x", 1)
    ex.set_inventory("b", "y", 1)
    tid = ex.propose_legs([("a", "b", "x", 1), ("b", "a", "y", 1)])
    ex.cancel(tid)
    assert ex.get("a", "x") == 1
    assert ex.get("b", "y") == 1
