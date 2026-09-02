from solution.order_book import OrderBook


def test_cancelling_the_middle_order_at_a_level_preserves_the_others_time_priority():
    book = OrderBook()
    book.limit("a", "SELL", 100, 3)
    book.limit("b", "SELL", 100, 3)
    book.limit("c", "SELL", 100, 3)

    assert book.cancel("b") is True

    fills = book.limit("taker", "BUY", 100, 6)
    assert fills == [
        {"maker_order_id": "a", "taker_order_id": "taker", "price": 100, "qty": 3},
        {"maker_order_id": "c", "taker_order_id": "taker", "price": 100, "qty": 3},
    ]


def test_cancelling_the_first_order_at_a_level_leaves_the_rest_in_order():
    book = OrderBook()
    book.limit("a", "SELL", 100, 3)
    book.limit("b", "SELL", 100, 3)
    book.limit("c", "SELL", 100, 3)

    assert book.cancel("a") is True

    fills = book.limit("taker", "BUY", 100, 6)
    assert fills == [
        {"maker_order_id": "b", "taker_order_id": "taker", "price": 100, "qty": 3},
        {"maker_order_id": "c", "taker_order_id": "taker", "price": 100, "qty": 3},
    ]


def test_cancelling_a_partially_filled_order_removes_only_its_remaining_quantity():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.limit("b1", "BUY", 100, 2)  # partially fills s1: 2 filled, 3 left resting

    assert book.cancel("s1") is True

    fills = book.limit("b2", "BUY", 100, 3)
    assert fills == []  # s1's remaining 3 were cancelled, nothing left to hit
    assert book.best_ask() is None


def test_cancel_is_idempotent():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    assert book.cancel("s1") is True
    assert book.cancel("s1") is False


def test_cancelling_the_only_order_at_the_best_ask_advances_to_the_next_level():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)
    book.limit("s2", "SELL", 105, 5)

    assert book.best_ask() == 100
    book.cancel("s1")
    assert book.best_ask() == 105


def test_cancelling_the_only_order_at_the_best_bid_advances_to_the_next_level():
    book = OrderBook()
    book.limit("b1", "BUY", 95, 5)
    book.limit("b2", "BUY", 90, 5)

    assert book.best_bid() == 95
    book.cancel("b1")
    assert book.best_bid() == 90


def test_cancelling_the_last_order_on_a_side_empties_it():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 5)

    book.cancel("s1")
    assert book.best_ask() is None


def test_correctness_holds_across_many_orders_and_scattered_cancellations():
    book = OrderBook()
    ids = [f"s{i}" for i in range(60)]
    for i, oid in enumerate(ids):
        # three price levels, 20 orders each, arriving in a mixed order
        price = 100 + (i % 3)
        book.limit(oid, "SELL", price, 1)

    # cancel every third order across all levels
    for oid in ids[::3]:
        assert book.cancel(oid) is True

    remaining = set(ids) - set(ids[::3])
    fills = book.limit("sweeper", "BUY", 102, len(remaining))
    filled_ids = {f["maker_order_id"] for f in fills}

    assert filled_ids == remaining
    assert book.best_ask() is None


def test_an_order_id_can_be_reused_once_it_is_no_longer_resting():
    book = OrderBook()
    book.limit("x", "SELL", 100, 1)
    book.cancel("x")

    book.limit("x", "SELL", 101, 1)

    assert book.best_ask() == 101
    assert book.cancel("x") is True


def test_market_orders_still_sweep_correctly_around_a_cancelled_middle_order():
    book = OrderBook()
    book.limit("s1", "SELL", 100, 3)
    book.limit("s2", "SELL", 100, 3)
    book.limit("s3", "SELL", 101, 3)

    book.cancel("s2")
    fills = book.market("m1", "BUY", 4)

    assert fills == [
        {"maker_order_id": "s1", "taker_order_id": "m1", "price": 100, "qty": 3},
        {"maker_order_id": "s3", "taker_order_id": "m1", "price": 101, "qty": 1},
    ]
    assert book.best_ask() == 101
