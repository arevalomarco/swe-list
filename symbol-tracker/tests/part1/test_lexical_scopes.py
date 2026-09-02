import pytest

from solution.symbol_tracker import SymbolTracker


def test_the_pad_worked_example():
    t = SymbolTracker()
    t.declare("g_count", "int")
    t.enter_scope("g")
    t.declare("x", "int")
    t.enter_scope("f")

    assert t.lookup("x") == "int"
    t.declare("x", "bool")
    assert t.lookup("x") == "bool"
    assert t.lookup("nope") is None
    with pytest.raises(ValueError):
        t.declare("x", "int")

    t.exit_scope()
    assert t.lookup("x") == "int"


def test_lookup_before_any_scope_is_entered_reads_root():
    t = SymbolTracker()
    t.declare("g_count", "int")

    assert t.lookup("g_count") == "int"
    assert t.lookup("nope") is None


def test_declare_and_lookup_in_the_same_scope():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")

    assert t.lookup("x") == "int"


def test_inner_scope_sees_outer_declaration():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.enter_scope("f")

    assert t.lookup("x") == "int"


def test_inner_declaration_shadows_outer_without_changing_it():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.enter_scope("f")
    t.declare("x", "bool")

    assert t.lookup("x") == "bool"

    t.exit_scope()
    assert t.lookup("x") == "int"  # g's x was never touched


def test_lookup_missing_name_returns_none():
    t = SymbolTracker()
    assert t.lookup("nope") is None


def test_declare_duplicate_name_in_same_scope_raises():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")

    with pytest.raises(ValueError):
        t.declare("x", "bool")


def test_exit_scope_at_root_raises():
    t = SymbolTracker()
    with pytest.raises(ValueError):
        t.exit_scope()


def test_enter_scope_same_id_twice_while_open_raises():
    t = SymbolTracker()
    t.enter_scope("g")

    with pytest.raises(ValueError):
        t.enter_scope("g")


def test_reentering_a_closed_scope_resumes_its_declarations():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("x", "int")
    t.exit_scope()

    t.enter_scope("g")
    assert t.lookup("x") == "int"


def test_reentering_a_scope_keeps_its_original_parent_not_the_new_caller():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("gv", "int")
    t.enter_scope("f")  # created here: parent is g
    t.exit_scope()
    t.exit_scope()

    t.enter_scope("h")  # sibling of g, parent is root
    t.declare("hv", "bool")
    t.enter_scope("f")  # resumed from h; parent is still g, not h

    assert t.lookup("gv") == "int"  # f -> g -> root still holds
    assert t.lookup("hv") is None  # h was never f's parent


def test_sibling_scopes_do_not_see_each_others_declarations():
    t = SymbolTracker()
    t.enter_scope("g")
    t.declare("gv", "int")
    t.exit_scope()

    t.enter_scope("h")
    assert t.lookup("gv") is None


def test_declaring_in_a_scope_does_not_affect_a_scope_entered_before_it():
    t = SymbolTracker()
    t.enter_scope("g")
    t.enter_scope("f")
    t.declare("x", "bool")
    t.exit_scope()

    assert t.lookup("x") is None  # g itself never declared x
