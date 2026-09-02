# In-Memory FS — Part 1

Unix-like paths. Root is `/`.

```python
fs = FS()
fs.mkdir("/a")
fs.write("/a/x", b"hi")
fs.read("/a/x")  # b"hi"
fs.ls("/a")      # ["x"]
```

## Requirements

- `FS()`
- `mkdir(path)` — parent must exist (no mkdir -p)
- `ls(path) -> list[str]` — child names; file path -> `ValueError`
- `write(path, data)` — create or overwrite file; parent must exist
- `read(path) -> bytes` — missing -> `ValueError`

Implement in `solution/fs.py`.
