"""
BBO / NBBO, Part 1

Resting quotes across exchanges. No matching — orders just rest.

- add(exchange_id, order_id, price, qty, side) — side in {"bid","ask"}.
- get_exchange_bbo(exchange_id) -> (best_bid, best_ask). None per empty side. Unknown exchange → (None, None).
- get_nbbo() -> (max bid, min ask) across exchanges.

Example:
book = MultiExchangeBook()
book.add("NYSE", "o1", 100, 10, "bid")
book.add("NYSE", "o2", 105, 5, "ask")
book.get_exchange_bbo("NYSE")  # (100, 105)
book.add("NASDAQ", "o3", 101, 1, "bid")
book.get_nbbo()                # (101, 105)

"""
class MultiExchangeBook:
    def add(self, exchange_id, order_id, price, qty, side):
        """side is 'bid' or 'ask'. Orders rest; nothing here crosses or fills."""
        raise NotImplementedError

    def get_exchange_bbo(self, exchange_id):
        """Return (best_bid, best_ask) for one exchange; None where a side is empty."""
        raise NotImplementedError

    def get_nbbo(self):
        """Return (max bid, min ask) across every exchange; None where no exchange has
        a resting order on that side at all."""
        raise NotImplementedError




"""
PART 2

Size at the best price.

- get_exchange_bbo_size(exchange_id) -> (bid_size, ask_size) — sum of qty at that exchange's own best bid / ask. 0 if empty on that side.
- get_nbbo_size() -> (bid_size, ask_size) — sum of qty across every exchange whose own best equals the NBBO price on that side.
- Tied NBBO prices: all tying exchanges contribute.

Example:
book.add("NYSE", "o1", 100, 10, "bid")
book.add("NYSE", "o2", 100, 4, "bid")
book.add("NYSE", "o3", 99, 999, "bid")
book.get_exchange_bbo_size("NYSE")  # (14, 0)
book.add("NASDAQ", "o4", 100, 6, "bid")
book.get_nbbo_size()                # (20, 0)

"""


"""
PART 3

cancel(order_id) -> bool.

- True if a resting order was removed, False if unknown or already cancelled (idempotent).
- Cancelling the only order at an exchange's best price advances that BBO (or to None).
- If that exchange set the NBBO, NBBO must move to the next best venue.
- Size helpers from part 2 must stay correct after cancel.

Example:
book.add("NYSE", "o1", 100, 10, "bid")
book.add("NASDAQ", "o2", 99, 5, "bid")
book.get_nbbo()  # (100, None)
book.cancel("o1")
book.get_exchange_bbo("NYSE")  # (None, None)
book.get_nbbo()                # (99, None)

"""
