# User API — Part 1

Small HTTP-ish router. Prefer separate classes over one giant handler.

```python
# POST /users with {username, email, password}
# 201 + {id, username, email} on success
# 400 on validation failure
# 409 on duplicate username
```

## Requirements

- `Request(method, path, body)` / `Response(status, body)`
- `UserValidator.validate(payload) -> None | error string`
  - require non-empty username, email, password; email must contain `@`
- `UserStore.create(username, email, password_hash) -> id` / `exists(username) -> bool`
- `UserController.create_user(payload) -> Response`
- `Router.dispatch(request) -> Response` — route `POST /users` to create; else 404

Implement in `solution/user_api.py`.
