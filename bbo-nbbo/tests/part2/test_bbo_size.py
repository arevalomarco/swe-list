from solution.bbo_nbbo import MultiExchangeBook


def test_exchange_bbo_size_sums_quantity_at_the_best_price_only():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NYSE", "o2", 100, 4, "bid")
    book.add("NYSE", "o3", 99, 999, "bid")  # a worse price — doesn't count

    assert book.get_exchange_bbo_size("NYSE") == (14, 0)


def test_exchange_bbo_size_is_zero_when_that_side_is_empty():
    book = MultiExchangeBook()

    assert book.get_exchange_bbo_size("NYSE") == (0, 0)  # never even seen an order


def test_bid_and_ask_bbo_sizes_are_independent():
    book = MultiExchangeBook()
    book.add("NYSE", "b1", 100, 3, "bid")
    book.add("NYSE", "a1", 105, 7, "ask")
    book.add("NYSE", "a2", 105, 2, "ask")

    assert book.get_exchange_bbo_size("NYSE") == (3, 9)


def test_the_worked_example_two_exchanges_tied_at_the_nbbo():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NYSE", "o2", 100, 4, "bid")
    book.add("NASDAQ", "o4", 100, 6, "bid")

    assert book.get_nbbo() == (100, None)
    assert book.get_nbbo_size() == (20, 0)


def test_nbbo_size_excludes_exchanges_not_quoting_the_nbbo_price():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")     # sets the NBBO bid
    book.add("NASDAQ", "o2", 99, 500, "bid")   # worse price, huge size — irrelevant

    assert book.get_nbbo() == (100, None)
    assert book.get_nbbo_size() == (10, 0)


def test_nbbo_size_is_zero_when_the_nbbo_side_is_none():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.get_nbbo() == (100, None)
    assert book.get_nbbo_size() == (10, 0)


def test_bbo_size_updates_after_a_new_order_deepens_the_best_level():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    assert book.get_exchange_bbo_size("NYSE") == (10, 0)

    book.add("NYSE", "o2", 100, 5, "bid")  # same price, deepens the level
    assert book.get_exchange_bbo_size("NYSE") == (15, 0)


def test_three_way_tie_at_the_nbbo_ask_sums_all_three():
    book = MultiExchangeBook()
    book.add("NYSE", "a1", 105, 2, "ask")
    book.add("NASDAQ", "a2", 105, 3, "ask")
    book.add("ARCA", "a3", 105, 4, "ask")
    book.add("ARCA", "a4", 106, 1000, "ask")  # deeper level at ARCA — irrelevant

    assert book.get_nbbo() == (None, 105)
    assert book.get_nbbo_size() == (0, 9)
