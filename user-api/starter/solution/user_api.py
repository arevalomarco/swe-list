"""User API — your implementation goes here."""


class Request:
    def __init__(self, method, path, body, headers=None):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers or {}


class Response:
    def __init__(self, status, body):
        self.status = status
        self.body = body


class UserValidator:
    def validate(self, payload):
        raise NotImplementedError


class UserStore:
    def create(self, username, email, password_hash):
        raise NotImplementedError

    def exists(self, username):
        raise NotImplementedError


class UserController:
    def __init__(self, validator, store, hash_fn=None):
        raise NotImplementedError

    def create_user(self, payload):
        raise NotImplementedError


class Router:
    def __init__(self, controller):
        raise NotImplementedError

    def dispatch(self, request):
        raise NotImplementedError

    def use(self, middleware):
        raise NotImplementedError
