# In-Memory FS — Part 2

```python
fs.rm("/a/x")
fs.rmdir("/a")  # requires empty dir
```

## Requirements

- `rm(path)` — remove a file; dir -> `ValueError` (use rmdir); missing -> `ValueError`
- `rmdir(path)` — empty directory only; non-empty / file / missing -> `ValueError`
