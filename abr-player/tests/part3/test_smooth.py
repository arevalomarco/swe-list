from solution.player import Player


class FakeAPI:
    def __init__(self, qualities, chunks, fetch_times, media_times):
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


def test_smooth_limits_drop_to_one_rung():
    # Without smooth: high -> low possible.
    # With max_step=1: high -> med only (cannot jump to low in one step),
    # even if low would also fit.
    api = FakeAPI(
        ["low", "med", "high"],
        [b"0", b"1"],
        {
            "low": [0.1, 0.5],
            "med": [0.1, 1.0],
            "high": [0.1, 5.0],
        },
        [2.0, 2.0],
    )
    got = Player(api).play_smooth(max_step=1)
    assert [q for q, _ in got] == ["high", "med"]


def test_play_no_underrun_still_works():
    api = FakeAPI(
        ["low", "high"],
        [b"0", b"1"],
        {"low": [0.5, 0.5], "high": [0.5, 0.5]},
        [2.0, 2.0],
    )
    got = Player(api).play_no_underrun()
    assert [q for q, _ in got] == ["high", "high"]
