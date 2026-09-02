# Symbol Tracker — Part 2

Touch scopes you are not standing in.

- `lookup(name, scope=None)` / `declare(name, typ, scope=None)`.
  Omit `scope` → current. Explicit `None` → root. Unknown id → `ValueError`.
- Exited scopes still exist for lookup/declare by id.
- `lookup` by id walks that scope's own chain, not yours.
- `declare(..., scope=target)` writes into target; the *current* scope redirects `name` to that binding.
  Raise if target already has the name, or current already has/binds it.

Example:
```python
t.enter_scope("g")
t.declare("x", "int")
t.enter_scope("f")
t.declare("x", "bool", None)  # root.x; f redirects x → root
t.lookup("x")                 # "bool"
t.lookup("x", "g")            # "int"
```
