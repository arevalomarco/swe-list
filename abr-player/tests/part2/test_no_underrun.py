import pytest

from solution.player import Player


class FakeAPI:
    def __init__(self, qualities, chunks, fetch_times, media_times):
        # fetch_times[q][i], media_times[i]
        self._qualities = list(qualities)
        self._chunks = list(chunks)
        self._fetch_times = fetch_times
        self._media_times = list(media_times)

    def qualities(self):
        return list(self._qualities)

    def num_chunks(self):
        return len(self._chunks)

    def fetch(self, quality, index):
        return self._chunks[index]

    def estimate_fetch_seconds(self, quality, index):
        return self._fetch_times[quality][index]

    def chunk_media_seconds(self, index):
        return self._media_times[index]


def test_startup_uses_highest_then_may_drop():
    # After chunk0 at high (media 2), buffered=2.
    # Chunk1: high needs 3 > 2, med needs 1.5 <= 2 -> med
    api = FakeAPI(
        ["low", "med", "high"],
        [b"0", b"1"],
        {
            "low": [0.5, 0.5],
            "med": [1.0, 1.5],
            "high": [2.0, 3.0],
        },
        [2.0, 2.0],
    )
    got = Player(api).play_no_underrun()
    assert [q for q, _ in got] == ["high", "med"]
    assert [d for _, d in got] == [b"0", b"1"]


def test_stays_high_when_estimates_fit():
    api = FakeAPI(
        ["low", "high"],
        [b"0", b"1", b"2"],
        {"low": [1, 1, 1], "high": [1, 1, 1]},
        [2, 2, 2],
    )
    got = Player(api).play_no_underrun()
    assert [q for q, _ in got] == ["high", "high", "high"]


def test_underrun_raises_when_even_lowest_too_slow():
    api = FakeAPI(
        ["low", "high"],
        [b"0", b"1"],
        {"low": [0.1, 10.0], "high": [0.1, 20.0]},
        [1.0, 1.0],
    )
    with pytest.raises(ValueError):
        Player(api).play_no_underrun()
