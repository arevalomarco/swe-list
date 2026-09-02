# Symbol Tracker — Part 3

Dynamic scopes resolve through whoever entered them this time, not their creation parent.

- `enter_scope(scope_id, dynamic=False)` — `dynamic` is consulted only on first creation; later resumes ignore it.
- Lexical scopes keep a fixed parent. Dynamic scopes use the current caller chain.
- `lookup` by id raises `ValueError` if resolving that scope (or any ancestor on the walk) hits a dynamic scope that is not currently open — even for the scope's own declarations.
- A lexical scope under a closed dynamic ancestor is also unaskable until that ancestor reopens.

Example:
```python
t.declare("x", "int")
t.enter_scope("d", dynamic=True)
t.exit_scope()
t.enter_scope("a"); t.declare("x", "bool")
t.enter_scope("d")
t.lookup("x")  # "bool" — via a
t.exit_scope(); t.exit_scope()
t.enter_scope("b")
t.enter_scope("d")
t.lookup("x")  # "int" — via b → root
```
