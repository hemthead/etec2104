import random

import common.contracts


def decide_order(trader_state, market_snapshot):
    return random_liquity(trader_state, market_snapshot)
    return common.contracts.make_order(
        trader_state["team"],
        common.contracts.SIDES[0],
        common.contracts.SYMBOLS[0],
        10,
        10,
    )
    return []  # order


# need to create strategies
def buylow_sell_high(trader_state, market_snapshot):
    pass
    # if price <= 100 -> buy
    # if price >= 103 -> sell


def make_markets(trader_state, market_snapshot):
    pass
    # this means you want to provide liquidity
    # to the market, so you would place bids
    # below ltp and asks above ltp.


def momentum(trader_state, market_snapshot):
    pass
    # join the wave...
    # if the market is trending up, be a buyer
    # down, be a seller.


def mean_reversion(trader_state, market_snapshot):
    pass
    # using a simple moving average, one can
    # decide to buy when the average crosses the
    # price going down, and sell the opposite


def random_liquity(trader_state, market_snapshot):
    return common.contracts.make_order(
        trader_state["team"],
        random.choice(common.contracts.SIDES),
        random.choice(common.contracts.SYMBOLS),
        random.randint(5, 15),
        random.randint(10, 100),
    )
    pass
    # just pick a range of numbers and buy/sell
    # to simply test your logic.
