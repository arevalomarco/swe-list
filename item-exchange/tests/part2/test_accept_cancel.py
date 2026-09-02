import pytest

from solution.item_exchange import Exchange


def _ready():
    ex = Exchange()
    ex.set_inventory("alice", "apple", 5)
    ex.set_inventory("bob", "coin", 10)
    tid = ex.propose("alice", "bob", "apple", 2, "coin", 3)
    return ex, tid


def test_accept_transfers_and_clears_reservation():
    ex, tid = _ready()
    ex.accept(tid)
    assert ex.get("alice", "apple") == 3
    assert ex.get("alice", "coin") == 3
    assert ex.get("bob", "apple") == 2
    assert ex.get("bob", "coin") == 7


def test_cancel_releases_reservation_without_transfer():
    ex, tid = _ready()
    ex.cancel(tid)
    assert ex.get("alice", "apple") == 5
    assert ex.get("bob", "coin") == 10
    assert ex.get("alice", "coin") == 0
    assert ex.get("bob", "apple") == 0


def test_double_accept_raises():
    ex, tid = _ready()
    ex.accept(tid)
    with pytest.raises(ValueError):
        ex.accept(tid)


def test_double_cancel_raises():
    ex, tid = _ready()
    ex.cancel(tid)
    with pytest.raises(ValueError):
        ex.cancel(tid)


def test_accept_after_cancel_raises():
    ex, tid = _ready()
    ex.cancel(tid)
    with pytest.raises(ValueError):
        ex.accept(tid)


def test_unknown_trade_raises():
    ex, _ = _ready()
    with pytest.raises(ValueError):
        ex.accept(999)


def test_cancel_frees_qty_for_a_new_propose():
    ex, tid = _ready()
    ex.cancel(tid)
    tid2 = ex.propose("alice", "bob", "apple", 5, "coin", 10)
    ex.accept(tid2)
    assert ex.get("alice", "apple") == 0
    assert ex.get("bob", "apple") == 5
