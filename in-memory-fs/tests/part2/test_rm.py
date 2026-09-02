import pytest
from solution.fs import FS


def test_rm_file():
    fs = FS()
    fs.write("/f", b"x")
    fs.rm("/f")
    with pytest.raises(ValueError):
        fs.read("/f")


def test_rm_on_dir_raises():
    fs = FS()
    fs.mkdir("/a")
    with pytest.raises(ValueError):
        fs.rm("/a")


def test_rmdir_empty():
    fs = FS()
    fs.mkdir("/a")
    fs.rmdir("/a")
    assert fs.ls("/") == []


def test_rmdir_nonempty():
    fs = FS()
    fs.mkdir("/a")
    fs.write("/a/x", b"1")
    with pytest.raises(ValueError):
        fs.rmdir("/a")


def test_rm_missing():
    fs = FS()
    with pytest.raises(ValueError):
        fs.rm("/nope")
