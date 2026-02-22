import random

from common import contracts


def decide_order(trader_state, market_snapshot) -> list:
    return random_liquity(trader_state, market_snapshot)

    return [
        common.contracts.make_order(
            trader_state["team"],
            common.contracts.sides[0],
            common.contracts.symbols[0],
            10,
            10,
        )
    ]
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


def random_liquity(trader_state, market_snapshot: dict[str, dict[str, float]]):
    orders = []

    for i in range(5):
        symbol = random.choice(contracts.SYMBOLS)
        side = random.choice(contracts.SIDES)

        last_price = market_snapshot["last_prices"][symbol]
        if last_price is None:
            last_price = 0

        print(symbol, last_price)

        price_offset = (random.random() - 0.5) * 3
        price_offset = random.randint(-3, 3)
        price = max(1.0, last_price + price_offset)
        qty = random.randint(1, 50)

        order = contracts.make_order(
            trader_state["team"],
            side,
            symbol,
            price,
            qty,
        )
        orders.append(order)

    return orders
    pass
    # just pick a range of numbers and buy/sell
    # to simply test your logic.
