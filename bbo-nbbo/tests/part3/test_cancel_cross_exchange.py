from solution.bbo_nbbo import MultiExchangeBook


def test_cancelling_the_orphan_best_bid_at_one_exchange_moves_that_exchanges_bbo_and_the_nbbo():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")   # NYSE's only bid — also the NBBO bid
    book.add("NASDAQ", "o2", 99, 5, "bid")
    assert book.get_nbbo() == (100, None)

    assert book.cancel("o1") is True

    assert book.get_exchange_bbo("NYSE") == (None, None)
    assert book.get_nbbo() == (99, None)  # moved to NASDAQ


def test_cancelling_an_order_not_at_the_best_price_leaves_both_bbos_unchanged():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")  # best
    book.add("NYSE", "o2", 95, 3, "bid")    # not best
    book.add("NASDAQ", "o3", 90, 1, "bid")

    assert book.cancel("o2") is True

    assert book.get_exchange_bbo("NYSE") == (100, None)
    assert book.get_nbbo() == (100, None)


def test_cancelling_the_best_ask_at_an_exchange_that_was_not_setting_the_nbbo():
    book = MultiExchangeBook()
    book.add("NYSE", "a1", 100, 5, "ask")   # sets the NBBO ask
    book.add("NASDAQ", "a2", 102, 5, "ask")  # worse — not setting the NBBO

    assert book.cancel("a2") is True

    assert book.get_exchange_bbo("NASDAQ") == (None, None)  # its own BBO did change
    assert book.get_nbbo() == (None, 100)                    # but the NBBO did not


def test_cancelling_one_of_two_exchanges_tied_at_the_nbbo_keeps_the_price_but_shrinks_the_size():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NASDAQ", "o2", 100, 6, "bid")
    assert book.get_nbbo() == (100, None)
    assert book.get_nbbo_size() == (16, 0)

    assert book.cancel("o2") is True

    assert book.get_nbbo() == (100, None)   # NYSE still quotes it
    assert book.get_nbbo_size() == (10, 0)  # but NASDAQ's share is gone


def test_cancelling_the_last_order_on_a_side_across_all_exchanges_sets_bbo_and_nbbo_to_none():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.cancel("o1") is True

    assert book.get_exchange_bbo("NYSE") == (None, None)
    assert book.get_nbbo() == (None, None)


def test_cancel_on_an_unknown_order_id_returns_false_and_changes_nothing():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.cancel("nope") is False
    assert book.get_exchange_bbo("NYSE") == (100, None)


def test_cancel_is_idempotent():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")

    assert book.cancel("o1") is True
    assert book.cancel("o1") is False


def test_cancelling_then_re_adding_at_a_better_price_moves_the_nbbo_again():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")
    book.add("NASDAQ", "o2", 99, 5, "bid")
    assert book.get_nbbo() == (100, None)

    book.cancel("o1")
    assert book.get_nbbo() == (99, None)

    book.add("NYSE", "o3", 102, 2, "bid")  # NYSE re-quotes, better than before
    assert book.get_nbbo() == (102, None)


def test_cancelling_a_middle_priced_order_at_the_nbbo_setting_exchange_leaves_the_nbbo_alone():
    book = MultiExchangeBook()
    book.add("NYSE", "o1", 100, 10, "bid")  # NYSE's best, and the NBBO
    book.add("NYSE", "o2", 98, 3, "bid")
    book.add("NASDAQ", "o3", 95, 1, "bid")

    assert book.cancel("o2") is True

    assert book.get_exchange_bbo("NYSE") == (100, None)
    assert book.get_nbbo() == (100, None)
