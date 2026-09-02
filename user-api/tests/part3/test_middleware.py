from solution.user_api import Request, Response, Router, UserController, UserStore, UserValidator


def make_router():
    return Router(UserController(UserValidator(), UserStore(), hash_fn=lambda p: p))


def test_auth_middleware_blocks():
    r = make_router()

    def auth(request, next):
        if request.headers.get("x-token") != "ok":
            return Response(401, {"error": "unauthorized"})
        return next(request)

    r.use(auth)
    denied = r.dispatch(Request("POST", "/users", {"username": "a", "email": "a@b.com", "password": "x"}))
    assert denied.status == 401
    ok = r.dispatch(Request(
        "POST", "/users",
        {"username": "a", "email": "a@b.com", "password": "x"},
        headers={"x-token": "ok"},
    ))
    assert ok.status == 201


def test_middleware_order_outer_first():
    r = make_router()
    order = []

    def a(request, next):
        order.append("a")
        return next(request)

    def b(request, next):
        order.append("b")
        return next(request)

    r.use(a)
    r.use(b)
    r.dispatch(Request("GET", "/nope", None, headers={"x-token": "ok"}))
    assert order == ["a", "b"]


def test_without_middleware_still_works():
    r = make_router()
    assert r.dispatch(Request("POST", "/users", {"username": "a", "email": "a@b.com", "password": "x"})).status == 201
