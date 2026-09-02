# User API — Part 3

Middleware chain on the router.

```python
def auth(request, next):
    if request.headers.get("x-token") != "ok":
        return Response(401, {"error": "unauthorized"})
    return next(request)

router.use(auth)
```

## Requirements

- `use(middleware)` where `middleware(request, next) -> Response`
- Order matters: first `use`d runs outermost (sees request first)
- `Request` gains optional `headers` dict (default `{}`)
