from solution.user_api import Request, Router, UserController, UserStore, UserValidator


def make_router(hash_fn=None):
    store = UserStore()
    return Router(UserController(UserValidator(), store, hash_fn=hash_fn)), store


def test_password_is_hashed():
    r, store = make_router(hash_fn=lambda p: "H:" + p)
    resp = r.dispatch(Request("POST", "/users", {"username": "a", "email": "a@b.com", "password": "secret"}))
    assert resp.status == 201
    user = store.get(resp.body["id"])
    assert user["password_hash"] == "H:secret"
    assert "password" not in resp.body
    assert "password_hash" not in resp.body


def test_get_user():
    r, _ = make_router(hash_fn=lambda p: p)
    created = r.dispatch(Request("POST", "/users", {"username": "a", "email": "a@b.com", "password": "x"}))
    resp = r.dispatch(Request("GET", f"/users/{created.body['id']}", None))
    assert resp.status == 200
    assert resp.body == {"id": created.body["id"], "username": "a", "email": "a@b.com"}


def test_get_missing():
    r, _ = make_router()
    assert r.dispatch(Request("GET", "/users/99", None)).status == 404


def test_create_still_works():
    r, _ = make_router()
    assert r.dispatch(Request("POST", "/users", {"username": "b", "email": "b@c.com", "password": "y"})).status == 201
