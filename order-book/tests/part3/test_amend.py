from solution.order_book import OrderBook


def test_amend_down_keeps_time_priority():
    book = OrderBook()
    book.limit("a", "SELL", 100, 5)
    book.limit("b", "SELL", 100, 5)

    assert book.amend("a", 2) is True

    fills = book.limit("t", "BUY", 100, 6)

    assert fills == [
        {"maker_order_id": "a", "taker_order_id": "t", "price": 100, "qty": 2},
        {"maker_order_id": "b", "taker_order_id": "t", "price": 100, "qty": 4},
    ]
    assert book.best_ask() == 100


def test_amend_to_zero_is_cancel():
    book = OrderBook()
    book.limit("a", "BUY", 50, 5)
    book.limit("b", "BUY", 50, 5)

    assert book.amend("a", 0) is True
    assert book.cancel("a") is False  # already gone — amend-to-zero already removed it

    fills = book.limit("s", "SELL", 50, 5)
    assert fills == [{"maker_order_id": "b", "taker_order_id": "s", "price": 50, "qty": 5}]


def test_amend_equal_qty_is_a_noop():
    book = OrderBook()
    book.limit("a", "SELL", 100, 5)

    assert book.amend("a", 5) is True
    fills = book.limit("t", "BUY", 100, 5)
    assert fills == [{"maker_order_id": "a", "taker_order_id": "t", "price": 100, "qty": 5}]


def test_amend_missing_id_returns_false():
    book = OrderBook()
    assert book.amend("nope", 1) is False


def test_amend_negative_qty_raises():
    book = OrderBook()
    book.limit("a", "SELL", 100, 2)
    try:
        book.amend("a", -1)
    except ValueError:
        return
    raise AssertionError("expected ValueError for negative new_qty")


def test_amend_grow_requeues_behind_everything_at_that_price():
    book = OrderBook()
    book.limit("a", "SELL", 100, 5)
    book.limit("b", "SELL", 100, 5)
    book.limit("c", "SELL", 100, 5)

    assert book.amend("a", 9) is True  # grow: succeeds, but "a" moves to the back

    fills = book.limit("t", "BUY", 100, 19)

    assert fills == [
        {"maker_order_id": "b", "taker_order_id": "t", "price": 100, "qty": 5},
        {"maker_order_id": "c", "taker_order_id": "t", "price": 100, "qty": 5},
        {"maker_order_id": "a", "taker_order_id": "t", "price": 100, "qty": 9},
    ]
    assert book.best_ask() is None


def test_amend_grow_does_not_change_price_or_side():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 3)
    book.limit("a", "BUY", 99, 2)  # rests, doesn't cross

    book.amend("a", 50)  # grow — large, but still resting at 99, still doesn't cross 100

    assert book.best_bid() == 99
    assert book.best_ask() == 100  # s1 untouched — amend never matches


def test_amend_on_a_fully_filled_order_returns_false():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.limit("b1", "BUY", 100, 5)  # fully fills s1

    assert book.amend("s1", 1) is False


def test_amend_on_a_market_order_id_returns_false_since_it_never_rested():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.market("m1", "BUY", 2)

    assert book.amend("m1", 1) is False


def test_amend_down_repeatedly_still_keeps_the_original_slot():
    book = OrderBook()
    book.limit("a", "SELL", 100, 10)
    book.limit("b", "SELL", 100, 10)

    book.amend("a", 5)
    book.amend("a", 1)  # shrink again — still in front

    fills = book.limit("t", "BUY", 100, 2)
    assert fills == [
        {"maker_order_id": "a", "taker_order_id": "t", "price": 100, "qty": 1},
        {"maker_order_id": "b", "taker_order_id": "t", "price": 100, "qty": 1},
    ]
