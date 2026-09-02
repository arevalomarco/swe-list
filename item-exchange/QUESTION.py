"""
Item Exchange, Part 1

Users hold item stacks. Propose an atomic swap that reserves inventory.

- Exchange()
- set_inventory(user, item, qty) — set that user's qty of item (qty >= 0).
- get(user, item) -> int — available qty (owned minus reserved). Missing -> 0.
- propose(buyer, seller, give_item, give_qty, take_item, take_qty) -> trade_id
  Reserves give_qty of give_item from buyer and take_qty of take_item from seller.
  Insufficient available on either side -> ValueError.

Example:
ex = Exchange()
ex.set_inventory("alice", "apple", 5)
ex.set_inventory("bob", "coin", 10)
tid = ex.propose("alice", "bob", "apple", 2, "coin", 3)
ex.get("alice", "apple")  # 3  — 2 reserved
ex.get("bob", "coin")     # 7

"""
class Exchange:
    def __init__(self):
        raise NotImplementedError

    def set_inventory(self, user, item, qty):
        raise NotImplementedError

    def get(self, user, item):
        raise NotImplementedError

    def propose(self, buyer, seller, give_item, give_qty, take_item, take_qty):
        raise NotImplementedError




"""
PART 2

Settle or drop a proposal.

- accept(trade_id) — move reserved balances:
  buyer loses give, gains take; seller loses take, gains give.
- cancel(trade_id) — release reservations; inventories unchanged aside from frees.
- Accept or cancel twice (or on unknown / already settled id) -> ValueError.
- After accept/cancel, reserved qty is gone from that trade.

ex.accept(tid)
ex.get("alice", "apple")  # 3
ex.get("alice", "coin")   # 3
ex.get("bob", "apple")    # 2
ex.get("bob", "coin")     # 7
ex.accept(tid)            # ValueError

"""


"""
PART 3

Multi-leg trades — all legs reserved or none.

- propose_legs(legs) -> trade_id where each leg is
  (from_user, to_user, item, qty).
- Reserve every leg; if any leg lacks available qty, roll back all reservations
  and raise ValueError.
- accept / cancel work on multi-leg trades the same way (atomic apply / release).

ex.set_inventory("a", "x", 1)
ex.set_inventory("b", "y", 1)
ex.set_inventory("c", "z", 1)
tid = ex.propose_legs([
    ("a", "b", "x", 1),
    ("b", "c", "y", 1),
    ("c", "a", "z", 1),
])
ex.accept(tid)
# a has z, b has x, c has y

"""
