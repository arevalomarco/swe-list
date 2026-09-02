class FakeAPI:
    def __init__(self, qualities, chunks):
        # chunks: list[bytes] — same payload at every quality for part 1
        self._qualities = list(qualities)
        self._chunks = list(chunks)

    def qualities(self):
        return list(self._qualities)

    def num_chunks(self):
        return len(self._chunks)

    def fetch(self, quality, index):
        assert quality in self._qualities
        return self._chunks[index]


from solution.player import Player


def test_play_max_quality_fetches_highest_in_order():
    api = FakeAPI(["low", "high"], [b"a", b"b", b"c"])
    got = Player(api).play_max_quality()
    assert got == [b"a", b"b", b"c"]


def test_empty_title():
    api = FakeAPI(["low", "high"], [])
    assert Player(api).play_max_quality() == []


def test_single_quality():
    api = FakeAPI(["only"], [b"x"])
    assert Player(api).play_max_quality() == [b"x"]
