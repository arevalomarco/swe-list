"""
Diff / Merge, Part 1

Line-level diff and apply over lists of strings.

- diff(old, new) — your format, whatever you like.
- apply(old, patch) replays patch against old and returns the result.
  Raise ValueError if patch does not apply cleanly to old.
- apply(old, diff(old, new)) == new

Example:
old = ["def f():", "    return 1"]
new = ["def f():", "    return 2"]
patch = diff(old, new)
apply(old, patch)  # ["def f():", "    return 2"]

"""
def diff(old_code: list[str], new_code: list[str]):
    """Return a diff from old_code to new_code — any representation you like."""
    raise NotImplementedError


def apply(old_code: list[str], patch) -> list[str]:
    """Replay `patch` against `old_code` and return the result."""
    raise NotImplementedError


def merge(base: list[str], mine: list[str], theirs: list[str], policy=None) -> list[str]:
    """Three-way merge. ConflictPolicy hooks in at part 3."""
    raise NotImplementedError




"""
PART 2

Three-way merge.

- merge(base, mine, theirs) -> list[str]
- Each side is an independent edit against base.
- Regions neither side touched come from base.
- Regions only one side touched take that side's version.
- Regions both sides changed the same way take that change once.
- Build merge using your diff / apply.

Example:
base = ["1", "2", "3", "4", "5"]
mine = ["1", "X", "3", "4", "5"]
theirs = ["1", "2", "3", "4", "Z"]
merge(base, mine, theirs)  # ["1", "X", "3", "4", "Z"]

"""


"""
PART 3

When mine and theirs disagree, ConflictPolicy decides what happens.

- merge(base, mine, theirs, policy=None). policy=None defaults to RaiseOnConflict().
- A conflict is different edits to the same base line, or different non-empty insertions at the same gap.
- One side deleting a line the other left alone is not a conflict — the line is gone.

Policies:

- RaiseOnConflict() — default. Any conflict raises ValueError.
- PreferMine() — on conflict, keep mine.
- PreferTheirs() — on conflict, keep theirs.
- Markers() — emit both sides wrapped in markers:

merge(base, ["1", "A", "2"], ["1", "B", "2"], policy=Markers())
# -> ["1", "<<<<<<< mine", "A", "=======", "B", ">>>>>>> theirs", "2"]

"""
