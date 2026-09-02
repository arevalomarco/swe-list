"""Symbol Tracker — your implementation goes here."""


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
