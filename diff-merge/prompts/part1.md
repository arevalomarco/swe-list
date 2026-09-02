# Diff / Merge — Part 1

Line-level diff and apply over lists of strings.

- `diff(old, new)` — your format, whatever you like.
- `apply(old, patch)` replays patch against old and returns the result.
  Raise `ValueError` if patch does not apply cleanly to old.
- `apply(old, diff(old, new)) == new`

Example:
```python
old = ["def f():", "    return 1"]
new = ["def f():", "    return 2"]
patch = diff(old, new)
apply(old, patch)  # ["def f():", "    return 2"]
```
