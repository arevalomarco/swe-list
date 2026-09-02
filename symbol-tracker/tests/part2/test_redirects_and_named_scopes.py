import pytest

from solution.symbol_tracker import SymbolTracker


def test_omitting_scope_still_means_current_scope():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")

    assert t.lookup("x") == "int"  # unchanged from part 1


def test_lookup_reaches_an_exited_scope_by_id():
    t = SymbolTracker()
    t.enter_scope("g")
    t.enter_scope("f")
    t.declare("y", "bool")
    t.exit_scope()  # back in g

    assert t.lookup("y", "f") == "bool"  # exited, still there
    assert t.lookup("y") is None  # g itself has no y


def test_lookup_by_id_resolves_from_that_scopes_own_chain_not_the_callers():
    t = SymbolTracker()
    t.enter_scope("g")
    t.enter_scope("f")
    t.declare("y", "bool")
    t.exit_scope()  # back in g

    t.enter_scope("h")  # sibling of f, never open at the same time as it
    assert t.lookup("y", "f") == "bool"  # across, not up


def test_lookup_unknown_scope_id_raises():
    t = SymbolTracker()
    with pytest.raises(ValueError):
        t.lookup("y", "nope")


def test_declare_unknown_scope_id_raises():
    t = SymbolTracker()
    with pytest.raises(ValueError):
        t.declare("x", "int", "nope")


def test_the_pad_worked_example_redirect_beats_a_nearer_declaration():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")  # g.x
    t.enter_scope("f")
    t.declare("x", "bool", None)  # root.x, and f now binds x to root

    assert t.lookup("x") == "bool"  # the redirect wins over g.x
    assert t.lookup("x", "g") == "int"  # g is untouched

    t.exit_scope()
    assert t.lookup("x") == "int"  # g never redirected anything


def test_declare_into_a_named_scope_creates_it_there_and_current_scope_redirects_to_it():
    t = SymbolTracker()
    t.enter_scope("g")
    t.enter_scope("h")  # sibling of g, not yet open at the same time
    t.exit_scope()

    t.enter_scope("f")  # sibling of g and h
    t.declare("x", "bool", "h")

    assert t.lookup("x", "h") == "bool"
    assert t.lookup("x") == "bool"  # f redirects to h


def test_declare_into_a_scope_that_already_has_the_name_raises():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.exit_scope()

    t.enter_scope("f")
    with pytest.raises(ValueError):
        t.declare("x", "bool", "g")


def test_declare_elsewhere_when_current_scope_already_binds_the_name_raises():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.exit_scope()

    t.enter_scope("f")
    t.declare("y", "bool", "g")  # f now binds y -> g

    with pytest.raises(ValueError):
        t.declare("y", "int")  # f already binds y


def test_declare_elsewhere_when_current_scope_already_owns_the_name_raises():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.exit_scope()

    t.enter_scope("f")
    t.declare("y", "bool")  # f owns y directly

    with pytest.raises(ValueError):
        t.declare("y", "int", "g")

    assert t.lookup("y", "g") is None  # the raising call wrote nothing into g either


def test_explicit_none_scope_targets_the_root_not_the_current_scope():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int", None)  # explicit None -> root, not g

    t.exit_scope()
    t.enter_scope("k")  # sibling of g, also a direct child of root

    # Only visible from a sibling that never touched g if the declaration truly landed on
    # root rather than on g itself (which explicit None could be mistaken for, since g was
    # the current scope at the time).
    assert t.lookup("x") == "int"
