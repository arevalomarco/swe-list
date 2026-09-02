"""
Order Book, Part 1

Limit order book. Price-time priority.

- A buy crosses the lowest resting sell with sell_price <= buy_price.
- A sell crosses the highest resting buy with buy_price >= sell_price.
- Fills happen at the resting order's price.
- Leftover quantity rests on the book.

- limit(order_id, side, price, qty) -> list of fills, in the order they happened.
  Each fill: {"maker_order_id", "taker_order_id", "price", "qty"}.
- market(order_id, side, qty) -> list of fills. Same matching loop, no price bound.
  Unfilled remainder is dropped, not rested. Against an empty opposite side -> [].
- best_bid() / best_ask() — best resting price, or None if that side is empty.
- cancel(order_id) -> bool — True if a resting order was removed, False otherwise.
  A linear scan is fine for this part.

Example:
book = OrderBook()
book.limit("s1", "SELL", 100, 5)
book.limit("s2", "SELL", 101, 5)
book.limit("b1", "BUY", 101, 7)
# -> [
#      {"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 5},
#      {"maker_order_id": "s2", "taker_order_id": "b1", "price": 101, "qty": 2},
#    ]
book.best_ask()  # 101
book.best_bid()  # None

"""
class OrderBook:
    def limit(self, order_id, side, price, qty):
        """side is 'BUY' or 'SELL'. Returns the list of fills this order produced."""
        raise NotImplementedError

    def market(self, order_id, side, qty):
        """Like limit, but with no price bound. Any unfilled remainder is dropped."""
        raise NotImplementedError

    def best_bid(self):
        raise NotImplementedError

    def best_ask(self):
        raise NotImplementedError

    def cancel(self, order_id):
        raise NotImplementedError




"""
PART 2

cancel(order_id) -> True if something was cancelled, False if it was not resting.

- Find a resting order without walking every level / every order at a level.
- Cancelling a middle order at a price must leave the remaining orders in the same time order.
- Cancelling a partially filled order removes only its remaining quantity.
- Cancelling the only order at the best price advances best_bid / best_ask.
- Cancel is idempotent. An order_id may be reused once it is no longer resting.

Example:
book.limit("a", "SELL", 100, 3)
book.limit("b", "SELL", 100, 3)
book.limit("c", "SELL", 100, 3)
book.cancel("b")  # True
book.limit("taker", "BUY", 100, 6)
# -> fills a, then c

"""


"""
PART 3

amend(order_id, new_qty) -> bool. True if a resting order was changed.

- Shrink keeps time priority.
- Grow re-queues at the back of that price. Same order_id. Does not match on the way in.
- new_qty == 0 is cancel.
- new_qty == current_qty is a successful no-op (True).
- Negative new_qty raises ValueError.
- Amend never changes price, so it can never cross.

Example:
book = OrderBook()
book.limit("a", "SELL", 100, 5)
book.limit("b", "SELL", 100, 5)
book.amend("a", 2)
book.limit("t", "BUY", 100, 6)
# -> fills 2 from a, then 4 from b

book.limit("c", "SELL", 100, 5)
book.amend("c", 9)
book.limit("t2", "BUY", 100, 5)
# -> b's remaining 1 fills before c

"""
