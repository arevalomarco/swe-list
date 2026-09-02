"""Item Exchange — your implementation goes here."""


class Exchange:
    def __init__(self):
        raise NotImplementedError

    def set_inventory(self, user, item, qty):
        raise NotImplementedError

    def get(self, user, item):
        raise NotImplementedError

    def propose(self, buyer, seller, give_item, give_qty, take_item, take_qty):
        raise NotImplementedError
