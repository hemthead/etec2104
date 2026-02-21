import random

from common import contracts
from exchange import exchange, persistence
from table import Table
from trader import strategy, trader_client


def run_simulation(num_ticks=50):
    random.seed(10)

    symbols = contracts.SYMBOLS

    try:
        state = persistence.load_exchange_state("exchange.json")
    except:
        state = exchange.create_exchange(symbols)

    trader = trader_client.create_trader(
        "dima", 1_000_000, {symbol: 1000 for symbol in contracts.SYMBOLS}
    )

    for step in range(num_ticks):
        print(f"Simulation step {step}")
        # periodically save state
        if step % 1 == 0:
            persistence.save_exchange_state(state, f"exchange-{step:02}.json")

        # right, so I guess get_market_snapshot shouldn't return anything...?
        snapshot = exchange.get_market_snapshot(state)
        print_snapshot(snapshot)

        order = strategy.decide_order(trader, snapshot)  # TODO: handle multiple orders
        trades = trader_client.submit_order(state, trader, order)
        print_trades(trades)
        trader_client.handle_fills(trader, trades)

        input()
        # update PnL
        # Log status
    print("Simulation finished")


def print_snapshot(market_snapshot):
    # return qty for price on side, or empty string if qty == 0; cells look nicer empty
    def get_qty(book, key, side):
        return book[str(key)][side] if book[str(key)][side] != 0 else ""

    COLOR_BID = "\033[30;34;1m"  # fg: black; bg: blue; bold
    COLOR_ASK = "\033[30;31;1m"  # fg: black; bg: red; bold
    COLOR_RST = "\033[0m"

    markets = market_snapshot["markets"]

    for symbol in markets.keys():
        prices = markets[symbol]
        # print(prices)

        table = Table(f"Market: {symbol}")
        table.add_val("Bids")
        table.add_val("Price")
        table.add_val("Asks")
        table.finish_row()

        for key in sorted(map(lambda x: float(x), prices.keys()), reverse=True):
            # |  bid_qty |    price |  ask_qty |
            table.add_val(get_qty(prices, key, "BUY"), color=COLOR_BID)
            table.add_val(key, ".2f")
            table.add_val(get_qty(prices, key, "SELL"), color=COLOR_ASK)
            table.finish_row()

        table.print()


def print_trades(trades):
    table = Table("Trades")
    table.add_val("Buyer")
    table.add_val("Seller")
    table.add_val("Symbol")
    table.add_val("Quantity")
    table.add_val("Price")
    table.finish_row()

    for trade in trades:
        table.add_val(trade["buyer"])
        table.add_val(trade["seller"])
        table.add_val(trade["symbol"])
        table.add_val(trade["qty"])
        table.add_val(trade["price"], ".2f")
        table.finish_row()

    table.print()


def main():
    run_simulation(num_ticks=7)


if __name__ == "__main__":
    main()
