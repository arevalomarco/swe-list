"""Diff / Merge — your implementation goes here."""


def diff(old_code: list[str], new_code: list[str]):
    """Return a diff from old_code to new_code — any representation you like."""
    raise NotImplementedError


def apply(old_code: list[str], patch) -> list[str]:
    """Replay `patch` against `old_code` and return the result."""
    raise NotImplementedError


def merge(base: list[str], mine: list[str], theirs: list[str], policy=None) -> list[str]:
    """Three-way merge. ConflictPolicy hooks in at part 3."""
    raise NotImplementedError
