# Symbol Tracker — Part 1

Nested scopes. Inner sees outer; inner declaration shadows outer.

- `enter_scope(scope_id)` — first enter creates the scope; parent is the current scope.
  Re-entering an already-open id raises `ValueError`. Re-entering a closed scope resumes it (parent unchanged).
- `exit_scope()` — `ValueError` at the root (`None`).
- `declare(name, typ)` in the current scope. Duplicate name in the same scope → `ValueError`.
- `lookup(name) -> typ | None`. Walk current scope up to root. Records nothing.

Example:
```python
t = SymbolTracker()
t.declare("g_count", "int")
t.enter_scope("g")
t.declare("x", "int")
t.enter_scope("f")
t.lookup("x")          # "int"
t.declare("x", "bool") # shadows
t.lookup("x")          # "bool"
t.exit_scope()
t.lookup("x")          # "int"
```
