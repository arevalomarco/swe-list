import pytest
from solution.fs import FS


def test_hard_link_shares_data():
    fs = FS()
    fs.mkdir("/a")
    fs.write("/a/x", b"hi")
    fs.link("/a/x", "/a/y")
    fs.write("/a/y", b"z")
    assert fs.read("/a/x") == b"z"


def test_unlink_keeps_data_via_other_name():
    fs = FS()
    fs.mkdir("/a")
    fs.write("/a/x", b"hi")
    fs.link("/a/x", "/a/y")
    fs.unlink("/a/x")
    assert fs.read("/a/y") == b"hi"
    with pytest.raises(ValueError):
        fs.read("/a/x")


def test_cannot_link_directory():
    fs = FS()
    fs.mkdir("/a")
    with pytest.raises(ValueError):
        fs.link("/a", "/b")


def test_link_requires_missing_new_name():
    fs = FS()
    fs.write("/x", b"1")
    fs.write("/y", b"2")
    with pytest.raises(ValueError):
        fs.link("/x", "/y")
