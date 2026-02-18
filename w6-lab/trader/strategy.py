def decide_order(trader_state, market_snapshot):
    return []  # order


# need to create strategies
def buylow_sell_high():
    pass
    # if price <= 100 -> buy
    # if price >= 103 -> sell


def make_markets():
    pass
    # this means you want to provide liquidity
    # to the market, so you would place bids
    # below ltp and asks above ltp.


def momentum():
    pass
    # join the wave...
    # if the market is trending up, be a buyer
    # down, be a seller.


def mean_reversion():
    pass
    # using a simple moving average, one can
    # decide to buy when the average crosses the
    # price going down, and sell the opposite


def random_liquity():
    pass
    # just pick a range of numbers and buy/sell
    # to simply test your logic.
