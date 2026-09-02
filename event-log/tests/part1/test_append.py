from solution.event_log import EventLog


def test_empty_log_has_no_events():
    log = EventLog()
    assert len(log) == 0
    assert log.all() == []


def test_append_preserves_insertion_order():
    log = EventLog()
    log.append("trade", {"px": 101.5})
    log.append("quote", {"bid": 101.0})

    assert len(log) == 2
    assert log.all() == [("trade", {"px": 101.5}), ("quote", {"bid": 101.0})]


def test_duplicate_types_are_kept_separately():
    log = EventLog()
    log.append("trade", 1)
    log.append("trade", 2)

    assert len(log) == 2
    assert log.all() == [("trade", 1), ("trade", 2)]


def test_all_does_not_expose_internal_storage():
    log = EventLog()
    log.append("trade", 1)

    log.all().append(("injected", 999))

    assert len(log) == 1
