"""
User API, Part 1

Small HTTP-ish router. Prefer separate classes over one giant handler.

# POST /users with {username, email, password}
# 201 + {id, username, email} on success
# 400 on validation failure
# 409 on duplicate username

- Request(method, path, body) / Response(status, body)
- UserValidator.validate(payload) -> None | error string
  - require non-empty username, email, password; email must contain @
- UserStore.create(username, email, password_hash) -> id / exists(username) -> bool
- UserController.create_user(payload) -> Response
- Router.dispatch(request) -> Response — route POST /users to create; else 404

"""
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




"""
PART 2

Hash password before store. Never store raw password.

# Controller takes hash_fn (e.g. lambda p: "h:" + p)
# GET /users/:id -> 200 + {id, username, email} or 404

- Inject hash_fn into controller (or store wiring); store only the hash
- UserStore.get(user_id) -> dict | None (may include hash internally)
- Response body for GET/create must not include password or password_hash
- Router handles GET /users/<id>

"""


"""
PART 3

Middleware chain on the router.

def auth(request, next):
    if request.headers.get("x-token") != "ok":
        return Response(401, {"error": "unauthorized"})
    return next(request)

router.use(auth)

- use(middleware) where middleware(request, next) -> Response
- Order matters: first used runs outermost (sees request first)
- Request gains optional headers dict (default {})

"""
