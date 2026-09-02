"""
Event Log, Part 1

Append-only in-memory log.

log = EventLog()
log.append("trade", {"px": 101.5})
log.append("quote", {"bid": 101.0})
len(log)   # 2
log.all()  # [("trade", {"px": 101.5}), ("quote", {"bid": 101.0})]

- append(event_type, payload) -> None
- all() -> list[tuple] — insertion order; must not expose mutable internal storage
- len(log) — event count

"""
from typing import Any


class EventLog:
    def __init__(self) -> None:
        raise NotImplementedError

    def append(self, event_type: str, payload: Any) -> None:
        raise NotImplementedError

    def all(self) -> list[tuple[str, Any]]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError




"""
PART 2

Query by type without scanning if you can index.

log.by_type("trade")  # [("trade", {"px": 101.5})]
log.by_type("fill")   # []

- by_type(event_type) -> list[tuple] — insertion order; unknown type -> []
- Returned list must not corrupt the log if mutated
- append must keep any index in sync

"""


"""
PART 3

Bounded log; oldest events drop when over capacity.

log = EventLog(capacity=2)
log.append("trade", 1)
log.append("trade", 2)
log.append("quote", 3)  # evicts ("trade", 1)
len(log)              # 2
log.by_type("trade")  # [("trade", 2)]

- EventLog(capacity=None) — None unbounded; raise if capacity < 1
- At capacity, append evicts the oldest event
- by_type must never return an evicted event

"""
