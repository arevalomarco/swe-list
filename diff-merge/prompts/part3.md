# Diff / Merge — Part 3

When mine and theirs disagree, `ConflictPolicy` decides what happens.

- `merge(base, mine, theirs, policy=None)`. `policy=None` defaults to `RaiseOnConflict()`.
- A conflict is different edits to the same base line, or different non-empty insertions at the same gap.
- One side deleting a line the other left alone is not a conflict — the line is gone.

Policies:

- `RaiseOnConflict()` — default. Any conflict raises `ValueError`.
- `PreferMine()` — on conflict, keep mine.
- `PreferTheirs()` — on conflict, keep theirs.
- `Markers()` — emit both sides wrapped in markers:

```python
merge(base, ["1", "A", "2"], ["1", "B", "2"], policy=Markers())
# -> ["1", "<<<<<<< mine", "A", "=======", "B", ">>>>>>> theirs", "2"]
```
