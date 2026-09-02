"""Order Book — your implementation goes here."""


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
