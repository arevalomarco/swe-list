import pytest

from solution.item_exchange import Exchange


def test_set_and_get_inventory():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 5)
    assert ex.get("alice", "apple") == 5
    assert ex.get("alice", "coin") == 0
    assert ex.get("bob", "apple") == 0


def test_propose_reserves_available_qty():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 5)
    ex.set_inventory("bob", "coin", 10)
    tid = ex.propose("alice", "bob", "apple", 2, "coin", 3)
    assert isinstance(tid, int)
    assert ex.get("alice", "apple") == 3
    assert ex.get("bob", "coin") == 7


def test_propose_insufficient_buyer_raises_and_reserves_nothing():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 1)
    ex.set_inventory("bob", "coin", 10)
    with pytest.raises(ValueError):
        ex.propose("alice", "bob", "apple", 2, "coin", 3)
    assert ex.get("alice", "apple") == 1
    assert ex.get("bob", "coin") == 10


def test_propose_insufficient_seller_rolls_back_buyer_reserve():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 5)
    ex.set_inventory("bob", "coin", 1)
    with pytest.raises(ValueError):
        ex.propose("alice", "bob", "apple", 2, "coin", 3)
    assert ex.get("alice", "apple") == 5
    assert ex.get("bob", "coin") == 1


def test_two_proposals_stack_reservations():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 5)
    ex.set_inventory("bob", "coin", 10)
    ex.propose("alice", "bob", "apple", 2, "coin", 3)
    ex.propose("alice", "bob", "apple", 1, "coin", 1)
    assert ex.get("alice", "apple") == 2
    assert ex.get("bob", "coin") == 6
