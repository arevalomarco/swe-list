# Diff / Merge — Part 2

Three-way merge.

- `merge(base, mine, theirs) -> list[str]`
- Each side is an independent edit against base.
- Regions neither side touched come from base.
- Regions only one side touched take that side's version.
- Regions both sides changed the same way take that change once.
- Build merge using your diff / apply.

Example:
```python
base = ["1", "2", "3", "4", "5"]
mine = ["1", "X", "3", "4", "5"]
theirs = ["1", "2", "3", "4", "Z"]
merge(base, mine, theirs)  # ["1", "X", "3", "4", "Z"]
```
