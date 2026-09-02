"""Token Manager — your implementation goes here."""


class TokenManager:
    def __init__(self, time_to_live):
        raise NotImplementedError

    def generate(self, token_id, current_time):
        raise NotImplementedError

    def renew(self, token_id, current_time):
        raise NotImplementedError

    def count_unexpired(self, current_time):
        raise NotImplementedError

    def acquire(self, resource_id, holder_id, current_time):
        raise NotImplementedError

    def renew_lease(self, resource_id, holder_id, fence, current_time):
        raise NotImplementedError
