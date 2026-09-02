from solution.bbo_nbbo import MultiExchangeBook


def test_the_worked_example():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NYSE", "o2", 105, 5, "ask")
    assert book.get_exchange_bbo("NYSE") == (100, 105)

    book.add("NASDAQ", "o3", 101, 1, "bid")
    assert book.get_nbbo() == (101, 105)


def test_exchange_bbo_is_none_on_both_sides_when_empty():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.get_exchange_bbo("NYSE") == (100, None)


def test_unknown_exchange_id_reads_as_an_empty_book():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.get_exchange_bbo("NASDAQ") == (None, None)


def test_exchange_bbo_picks_the_highest_bid_and_lowest_ask_at_that_exchange():
    book = MultiExchangeBook()
    book.add("NYSE", "b1", 50, 1, "bid")
    book.add("NYSE", "b2", 52, 1, "bid")  # higher — best bid
    book.add("NYSE", "b3", 51, 1, "bid")
    book.add("NYSE", "a1", 102, 1, "ask")
    book.add("NYSE", "a2", 100, 1, "ask")  # lower — best ask
    book.add("NYSE", "a3", 101, 1, "ask")

    assert book.get_exchange_bbo("NYSE") == (52, 100)


def test_nbbo_is_none_on_a_side_when_no_exchange_has_a_resting_order_there():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.get_nbbo() == (100, None)


def test_nbbo_bid_is_the_max_bid_across_exchanges():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NASDAQ", "o2", 103, 5, "bid")
    book.add("ARCA", "o3", 99, 5, "bid")

    assert book.get_nbbo() == (103, None)


def test_nbbo_ask_is_the_min_ask_across_exchanges():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 105, 10, "ask")
    book.add("NASDAQ", "o2", 102, 5, "ask")
    book.add("ARCA", "o3", 110, 5, "ask")

    assert book.get_nbbo() == (None, 102)


def test_nbbo_reflects_the_single_best_exchange_even_when_others_are_worse():
    book = MultiExchangeBook()
    book.add("NYSE", "b1", 100, 1, "bid")
    book.add("NYSE", "a1", 110, 1, "ask")
    book.add("NASDAQ", "b2", 90, 1, "bid")
    book.add("NASDAQ", "a2", 108, 1, "ask")

    assert book.get_nbbo() == (100, 108)


def test_multiple_orders_at_the_same_exchange_and_price_do_not_change_the_best_price():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NYSE", "o2", 100, 5, "bid")
    book.add("NYSE", "o3", 100, 1, "bid")

    assert book.get_exchange_bbo("NYSE") == (100, None)


def test_a_new_better_priced_order_updates_the_exchange_bbo_immediately():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    assert book.get_exchange_bbo("NYSE") == (100, None)

    book.add("NYSE", "o2", 101, 5, "bid")  # better bid
    assert book.get_exchange_bbo("NYSE") == (101, None)


def test_nbbo_updates_when_a_new_exchange_posts_a_better_price():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    assert book.get_nbbo() == (100, None)

    book.add("NASDAQ", "o2", 104, 3, "bid")
    assert book.get_nbbo() == (104, None)


def test_bid_and_ask_are_tracked_independently_per_exchange():
    book = MultiExchangeBook()
    book.add("NYSE", "b1", 100, 1, "bid")   # NYSE only ever quotes a bid
    book.add("NASDAQ", "a1", 105, 1, "ask")  # NASDAQ only ever quotes an ask

    assert book.get_exchange_bbo("NYSE") == (100, None)
    assert book.get_exchange_bbo("NASDAQ") == (None, 105)
    assert book.get_nbbo() == (100, 105)
