"""
In-Memory FS, Part 1

Unix-like paths. Root is /.

fs = FS()
fs.mkdir("/a")
fs.write("/a/x", b"hi")
fs.read("/a/x")  # b"hi"
fs.ls("/a")      # ["x"]

- FS()
- mkdir(path) — parent must exist (no mkdir -p)
- ls(path) -> list[str] — child names; file path -> ValueError
- write(path, data) — create or overwrite file; parent must exist
- read(path) -> bytes — missing -> ValueError

"""
class FS:
    def mkdir(self, path):
        raise NotImplementedError

    def ls(self, path):
        raise NotImplementedError

    def write(self, path, data):
        raise NotImplementedError

    def read(self, path):
        raise NotImplementedError

    def rm(self, path):
        raise NotImplementedError

    def rmdir(self, path):
        raise NotImplementedError

    def link(self, existing, new_path):
        raise NotImplementedError

    def unlink(self, path):
        raise NotImplementedError




"""
PART 2

fs.rm("/a/x")
fs.rmdir("/a")  # requires empty dir

- rm(path) — remove a file; dir -> ValueError (use rmdir); missing -> ValueError
- rmdir(path) — empty directory only; non-empty / file / missing -> ValueError

"""


"""
PART 3

Hard links.

fs.link("/a/x", "/a/y")
fs.write("/a/y", b"z")
fs.read("/a/x")  # b"z"
fs.unlink("/a/x")  # name gone; data remains via /a/y

- link(existing, new_path) — same inode/data; parent of new_path must exist; new name must not exist
- write via either path visible via the other
- unlink(path) removes a name; data freed when last link gone
- cannot link a directory (raise ValueError)
- rm may alias unlink for files

"""
