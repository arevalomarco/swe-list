from solution.event_log import EventLog


def test_capacity_none_is_unbounded():
    log = EventLog(capacity=None)
    for i in range(50):
        log.append("trade", i)

    assert len(log) == 50


def test_oldest_event_is_evicted_at_capacity():
    log = EventLog(capacity=2)
    log.append("trade", 1)
    log.append("trade", 2)
    log.append("quote", 3)

    assert len(log) == 2
    assert log.all() == [("trade", 2), ("quote", 3)]


def test_eviction_updates_type_lookup():
    # The point of the part: an index built in part 2 must not hand back evicted events.
    log = EventLog(capacity=2)
    log.append("trade", 1)
    log.append("trade", 2)
    log.append("quote", 3)

    assert log.by_type("trade") == [("trade", 2)]


def test_type_disappears_once_all_its_events_are_evicted():
    log = EventLog(capacity=1)
    log.append("trade", 1)
    log.append("quote", 2)

    assert log.by_type("trade") == []
    assert log.by_type("quote") == [("quote", 2)]
