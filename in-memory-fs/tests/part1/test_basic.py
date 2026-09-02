import pytest
from solution.fs import FS


def test_pad_example():
    fs = FS()
    fs.mkdir("/a")
    fs.write("/a/x", b"hi")
    assert fs.read("/a/x") == b"hi"
    assert fs.ls("/a") == ["x"]


def test_ls_root():
    fs = FS()
    fs.mkdir("/a")
    fs.mkdir("/b")
    assert fs.ls("/") == ["a", "b"]


def test_write_requires_parent():
    fs = FS()
    with pytest.raises(ValueError):
        fs.write("/a/x", b"hi")


def test_mkdir_requires_parent():
    fs = FS()
    with pytest.raises(ValueError):
        fs.mkdir("/a/b")


def test_read_missing():
    fs = FS()
    with pytest.raises(ValueError):
        fs.read("/nope")


def test_ls_on_file():
    fs = FS()
    fs.write("/f", b"x")
    with pytest.raises(ValueError):
        fs.ls("/f")


def test_overwrite():
    fs = FS()
    fs.write("/f", b"a")
    fs.write("/f", b"b")
    assert fs.read("/f") == b"b"
