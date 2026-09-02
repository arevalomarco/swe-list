"""BBO / NBBO — your implementation goes here."""


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
