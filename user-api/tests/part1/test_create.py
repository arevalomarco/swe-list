from solution.user_api import Request, Router, UserController, UserStore, UserValidator


def make_router():
    return Router(UserController(UserValidator(), UserStore()))


def test_create_success():
    r = make_router()
    resp = r.dispatch(Request("POST", "/users", {"username": "a", "email": "a@b.com", "password": "x"}))
    assert resp.status == 201
    assert resp.body["username"] == "a"
    assert resp.body["email"] == "a@b.com"
    assert "id" in resp.body


def test_validation_failure():
    r = make_router()
    resp = r.dispatch(Request("POST", "/users", {"username": "", "email": "a@b.com", "password": "x"}))
    assert resp.status == 400


def test_invalid_email():
    r = make_router()
    resp = r.dispatch(Request("POST", "/users", {"username": "a", "email": "nope", "password": "x"}))
    assert resp.status == 400


def test_duplicate_username():
    r = make_router()
    body = {"username": "a", "email": "a@b.com", "password": "x"}
    assert r.dispatch(Request("POST", "/users", body)).status == 201
    assert r.dispatch(Request("POST", "/users", body)).status == 409


def test_unknown_route():
    r = make_router()
    assert r.dispatch(Request("GET", "/nope", None)).status == 404
