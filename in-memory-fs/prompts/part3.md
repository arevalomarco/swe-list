# In-Memory FS — Part 3

Hard links.

```python
fs.link("/a/x", "/a/y")
fs.write("/a/y", b"z")
fs.read("/a/x")  # b"z"
fs.unlink("/a/x")  # name gone; data remains via /a/y
```

## Requirements

- `link(existing, new_path)` — same inode/data; parent of new_path must exist; new name must not exist
- write via either path visible via the other
- `unlink(path)` removes a name; data freed when last link gone
- cannot `link` a directory (raise `ValueError`)
- `rm` may alias `unlink` for files
