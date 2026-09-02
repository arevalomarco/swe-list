import pytest

from solution.symbol_tracker import SymbolTracker


def test_dynamic_scope_has_its_own_declarations_like_any_scope():
    t = SymbolTracker()
    t.enter_scope("d", dynamic=True)
    t.declare("y", "str")

    assert t.lookup("y") == "str"


def test_dynamic_scope_resolves_through_the_caller_that_entered_it():
    t = SymbolTracker()
    t.declare("x", "int")  # root.x
    t.enter_scope("d", dynamic=True)
    t.declare("y", "str")
    t.exit_scope()

    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("d")  # entered from a

    assert t.lookup("x") == "bool"  # resolves a -> root
    assert t.lookup("y") == "str"  # d's own, always


def test_same_dynamic_scope_resolves_differently_through_a_different_caller():
    t = SymbolTracker()
    t.declare("x", "int")  # root.x
    t.enter_scope("d", dynamic=True)
    t.exit_scope()

    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("d")  # entered from a
    assert t.lookup("x") == "bool"
    t.exit_scope()
    t.exit_scope()

    t.enter_scope("b")  # b declares no x
    t.enter_scope("d")  # the same scope, entered from b this time

    assert t.lookup("x") == "int"  # resolves b -> root, not a -> root


def test_lexical_scope_created_inside_dynamic_keeps_its_own_fixed_parent():
    t = SymbolTracker()
    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("d", dynamic=True)  # dynamic, entered from a
    t.enter_scope("c")  # lexical, created here -- parent is d, forever

    assert t.lookup("x") == "bool"  # c -> d -> a -> root


def test_dynamic_scope_not_currently_open_raises_on_lookup_by_id():
    t = SymbolTracker()
    t.enter_scope("d", dynamic=True)
    t.declare("y", "str")
    t.exit_scope()

    with pytest.raises(ValueError):
        t.lookup("x", "d")


def test_dynamic_scopes_own_declaration_is_unreachable_while_closed():
    t = SymbolTracker()
    t.enter_scope("d", dynamic=True)
    t.declare("y", "str")
    t.exit_scope()

    # d has y right there in its own table, but a closed dynamic scope cannot answer for
    # itself at all -- the chain behind it is unknown, and one answer can't be half-given.
    with pytest.raises(ValueError):
        t.lookup("y", "d")


def test_lexical_scope_under_a_closed_dynamic_ancestor_raises():
    t = SymbolTracker()
    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("d", dynamic=True)  # dynamic, entered from a
    t.enter_scope("c")  # lexical, created here -- parent is d, forever
    t.exit_scope()  # leave c
    t.exit_scope()  # leave d
    t.exit_scope()  # leave a -- c, d, and a are all closed now

    # c itself never moved and doesn't need to be open -- the walk simply can't get past
    # its closed dynamic ancestor d without knowing who is currently running it.
    with pytest.raises(ValueError):
        t.lookup("x", "c")


def test_lexical_scope_under_a_reopened_dynamic_ancestor_resolves_through_the_new_caller():
    t = SymbolTracker()
    t.declare("x", "int")  # root.x
    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("d", dynamic=True)  # entered from a
    t.enter_scope("c")  # lexical, parent is d, forever
    t.exit_scope()
    t.exit_scope()
    t.exit_scope()  # back to root; c, d, a all closed

    t.enter_scope("b")  # b declares no x
    t.enter_scope("d")  # d resumed, entered from b this time

    assert t.lookup("x", "c") == "int"  # c -> d -> b -> root, not a's "bool"


def test_dynamic_flag_is_ignored_on_a_later_entry_that_resumes_the_scope():
    t = SymbolTracker()
    t.declare("x", "int")  # root.x
    t.enter_scope("d", dynamic=True)
    t.exit_scope()

    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("d")  # default dynamic=False on resume -- does not un-dynamic it

    assert t.lookup("x") == "bool"  # still resolves through the caller (a), not fixed


def test_dynamic_flag_passed_on_resume_of_a_lexical_scope_is_ignored_too():
    t = SymbolTracker()
    t.declare("x", "int")  # root.x
    t.enter_scope("e")  # created lexical (the default)
    t.exit_scope()

    t.enter_scope("a")
    t.declare("x", "bool")
    t.enter_scope("e", dynamic=True)  # resumed; e stays lexical, parent is root, not a

    assert t.lookup("x") == "int"  # e -> root, unaffected by being entered from a


def test_reentering_an_already_open_dynamic_scope_raises_same_as_any_scope():
    t = SymbolTracker()
    t.enter_scope("d", dynamic=True)

    with pytest.raises(ValueError):
        t.enter_scope("d")


def test_parts_one_and_two_still_hold_alongside_dynamic_scopes():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.enter_scope("f")
    t.declare("x", "bool", None)  # root.x, and f now binds x to root

    assert t.lookup("x") == "bool"
    assert t.lookup("x", "g") == "int"

    t.enter_scope("d", dynamic=True)
    t.declare("z", "float")
    assert t.lookup("z") == "float"
    assert t.lookup("x") == "bool"  # d -> f -> root's redirect, unaffected by dynamic-ness
