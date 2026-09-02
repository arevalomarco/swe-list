# User API — Part 2

Hash password before store. Never store raw password.

```python
# Controller takes hash_fn (e.g. lambda p: "h:" + p)
# GET /users/:id -> 200 + {id, username, email} or 404
```

## Requirements

- Inject `hash_fn` into controller (or store wiring); store only the hash
- `UserStore.get(user_id) -> dict | None` (may include hash internally)
- Response body for GET/create must **not** include password or password_hash
- `Router` handles `GET /users/<id>`
