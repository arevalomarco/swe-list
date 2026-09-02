"""Feed Sync — your implementation goes here."""


class FeedSync:
    def __init__(self, skew_ms=0):
        raise NotImplementedError

    def on_a(self, ts, side, price, qty, seq=None):
        raise NotImplementedError

    def on_b(self, ts, side, price, qty, seq=None):
        raise NotImplementedError

    def discrepancies(self):
        raise NotImplementedError

    def recover(self, feed):
        raise NotImplementedError
