from solution.event_log import EventLog


def test_by_type_returns_only_matching_events():
    log = EventLog()
    log.append("trade", 1)
    log.append("quote", 2)
    log.append("trade", 3)

    assert log.by_type("trade") == [("trade", 1), ("trade", 3)]
    assert log.by_type("quote") == [("quote", 2)]


def test_unknown_type_returns_empty_list():
    log = EventLog()
    log.append("trade", 1)

    assert log.by_type("fill") == []


def test_by_type_on_empty_log():
    assert EventLog().by_type("trade") == []


def test_by_type_does_not_expose_internal_storage():
    log = EventLog()
    log.append("trade", 1)

    log.by_type("trade").append(("injected", 999))

    assert log.by_type("trade") == [("trade", 1)]
