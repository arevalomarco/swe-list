from solution.order_book import OrderBook


def test_a_resting_order_does_not_cross_when_nothing_matches():
    book = OrderBook()
    fills = book.limit("s1", "SELL", 100, 5)

    assert fills == []
    assert book.best_ask() == 100
    assert book.best_bid() is None


def test_a_buy_below_the_ask_does_not_cross():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    fills = book.limit("b1", "BUY", 99, 5)

    assert fills == []
    assert book.best_bid() == 99
    assert book.best_ask() == 100


def test_a_full_match_fills_at_the_resting_price():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    fills = book.limit("b1", "BUY", 100, 5)

    assert fills == [{"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 5}]
    assert book.best_ask() is None
    assert book.best_bid() is None


def test_a_partial_fill_rests_the_remainder():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    fills = book.limit("b1", "BUY", 100, 8)

    assert fills == [{"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 5}]
    assert book.best_ask() is None
    assert book.best_bid() == 100  # 3 units of b1 rest


def test_fills_at_the_resting_price_not_the_taker_price():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    fills = book.limit("b1", "BUY", 110, 5)  # b1 would pay up to 110, but fills at 100

    assert fills == [{"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 5}]


def test_the_worked_example_sweeps_two_price_levels():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.limit("s2", "SELL", 101, 5)

    fills = book.limit("b1", "BUY", 101, 7)

    assert fills == [
        {"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 5},
        {"maker_order_id": "s2", "taker_order_id": "b1", "price": 101, "qty": 2},
    ]
    assert book.best_ask() == 101  # s2 has 3 left
    assert book.best_bid() is None  # b1 fully filled


def test_time_priority_within_one_price_level():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 3)
    book.limit("s2", "SELL", 100, 3)  # same price, arrived second

    fills = book.limit("b1", "BUY", 100, 4)

    assert fills == [
        {"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 3},
        {"maker_order_id": "s2", "taker_order_id": "b1", "price": 100, "qty": 1},
    ]


def test_sell_side_crosses_the_highest_resting_buy_first():
    book = OrderBook()
    book.limit("b1", "BUY", 99, 5)
    book.limit("b2", "BUY", 100, 5)  # better price, should fill first even though listed second

    fills = book.limit("s1", "SELL", 99, 7)

    assert fills == [
        {"maker_order_id": "b2", "taker_order_id": "s1", "price": 100, "qty": 5},
        {"maker_order_id": "b1", "taker_order_id": "s1", "price": 99, "qty": 2},
    ]


def test_best_bid_and_best_ask_track_multiple_resting_levels():
    book = OrderBook()
    book.limit("s1", "SELL", 102, 1)
    book.limit("s2", "SELL", 100, 1)  # lower — should be the best ask
    book.limit("s3", "SELL", 101, 1)
    book.limit("b1", "BUY", 50, 1)
    book.limit("b2", "BUY", 52, 1)   # higher — should be the best bid
    book.limit("b3", "BUY", 51, 1)

    assert book.best_ask() == 100
    assert book.best_bid() == 52


def test_cancel_removes_a_resting_order_so_it_cannot_fill():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.limit("s2", "SELL", 101, 5)

    assert book.cancel("s1") is True

    fills = book.limit("b1", "BUY", 101, 5)
    assert fills == [{"maker_order_id": "s2", "taker_order_id": "b1", "price": 101, "qty": 5}]
    assert book.best_ask() is None


def test_cancel_on_an_unknown_order_id_returns_false():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    assert book.cancel("nope") is False
    assert book.best_ask() == 100


def test_cancel_on_an_already_fully_filled_order_returns_false():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.limit("b1", "BUY", 100, 5)  # fully fills s1

    assert book.cancel("s1") is False


def test_multiple_partial_fills_across_several_resting_orders():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 2)
    book.limit("s2", "SELL", 100, 2)
    book.limit("s3", "SELL", 100, 2)

    fills = book.limit("b1", "BUY", 100, 5)

    assert fills == [
        {"maker_order_id": "s1", "taker_order_id": "b1", "price": 100, "qty": 2},
        {"maker_order_id": "s2", "taker_order_id": "b1", "price": 100, "qty": 2},
        {"maker_order_id": "s3", "taker_order_id": "b1", "price": 100, "qty": 1},
    ]
    assert book.best_ask() == 100  # s3 has 1 left


def test_market_order_sweeps_multiple_price_levels():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 3)
    book.limit("s2", "SELL", 101, 3)

    fills = book.market("m1", "BUY", 5)

    assert fills == [
        {"maker_order_id": "s1", "taker_order_id": "m1", "price": 100, "qty": 3},
        {"maker_order_id": "s2", "taker_order_id": "m1", "price": 101, "qty": 2},
    ]
    assert book.best_ask() == 101  # s2 has 1 left


def test_market_order_partial_fill_drops_the_remainder_instead_of_resting():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 3)

    fills = book.market("m1", "BUY", 10)

    assert fills == [{"maker_order_id": "s1", "taker_order_id": "m1", "price": 100, "qty": 3}]
    assert book.best_ask() is None
    assert book.best_bid() is None  # the other 7 units never rested


def test_market_order_against_an_empty_book_returns_no_fills():
    book = OrderBook()
    assert book.market("m1", "BUY", 5) == []
    assert book.best_bid() is None
    assert book.best_ask() is None


def test_market_sell_crosses_the_highest_resting_buy_first():
    book = OrderBook()
    book.limit("b1", "BUY", 99, 3)
    book.limit("b2", "BUY", 100, 3)

    fills = book.market("m1", "SELL", 4)

    assert fills == [
        {"maker_order_id": "b2", "taker_order_id": "m1", "price": 100, "qty": 3},
        {"maker_order_id": "b1", "taker_order_id": "m1", "price": 99, "qty": 1},
    ]


def test_market_order_never_appears_in_best_bid_or_best_ask():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 1)

    book.market("m1", "BUY", 1)  # fully fills and consumes s1
    assert book.best_bid() is None
    assert book.best_ask() is None


def test_cancelling_a_market_order_id_is_a_no_op_since_it_never_rested():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.market("m1", "BUY", 2)

    assert book.cancel("m1") is False
