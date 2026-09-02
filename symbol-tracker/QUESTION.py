"""
Symbol Tracker, Part 1

Nested scopes. Inner sees outer; inner declaration shadows outer.

- enter_scope(scope_id) — first enter creates the scope; parent is the current scope.
  Re-entering an already-open id raises ValueError. Re-entering a closed scope resumes it (parent unchanged).
- exit_scope() — ValueError at the root (None).
- declare(name, typ) in the current scope. Duplicate name in the same scope → ValueError.
- lookup(name) -> typ | None. Walk current scope up to root. Records nothing.

Example:
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

"""
class SymbolTracker:
    def enter_scope(self, scope_id):
        raise NotImplementedError

    def exit_scope(self):
        """Leave the current scope. ValueError at the root."""
        raise NotImplementedError

    def declare(self, name, typ):
        """Declare in the current scope."""
        raise NotImplementedError

    def lookup(self, name):
        """Type of the binding visible from the current scope, or None.

        Records nothing.
        """
        raise NotImplementedError




"""
PART 2

Touch scopes you are not standing in.

- lookup(name, scope=None) / declare(name, typ, scope=None).
  Omit scope → current. Explicit None → root. Unknown id → ValueError.
- Exited scopes still exist for lookup/declare by id.
- lookup by id walks that scope's own chain, not yours.
- declare(..., scope=target) writes into target; the current scope redirects name to that binding.
  Raise if target already has the name, or current already has/binds it.

Example:
t.enter_scope("g")
t.declare("x", "int")
t.enter_scope("f")
t.declare("x", "bool", None)  # root.x; f redirects x → root
t.lookup("x")                 # "bool"
t.lookup("x", "g")            # "int"

"""


"""
PART 3

Dynamic scopes resolve through whoever entered them this time, not their creation parent.

- enter_scope(scope_id, dynamic=False) — dynamic is consulted only on first creation; later resumes ignore it.
- Lexical scopes keep a fixed parent. Dynamic scopes use the current caller chain.
- lookup by id raises ValueError if resolving that scope (or any ancestor on the walk) hits a dynamic scope that is not currently open — even for the scope's own declarations.
- A lexical scope under a closed dynamic ancestor is also unaskable until that ancestor reopens.

Example:
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

"""
