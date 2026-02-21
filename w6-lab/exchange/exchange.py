import common.contracts as contracts
import exchange.matching as matching

books = {}

last_prices = {}

trade_log = []


def create_exchange(symbols):
    state = {"last_prices": {}, "books": {}, "trade_log": list()}
    for symbol in symbols:
        state["books"].setdefault(symbol, {"BUY": list(), "SELL": list()})
        state["last_prices"].setdefault(symbol, None)
    return state


def place_order(state, order):
    order_book = state["books"][order["symbol"]]
    matching.insert_order(order_book, order)

    trades = matching.match_orders(state, order["symbol"])
    apply_trades_to_state(state, trades)

    return trades  # trades


def get_market_snapshot(state: dict[str, dict[str, dict]]):
    # I think I'm supposed to collapse orders into just price brackets here...
    markets: dict[str, dict[str, dict[str, int]]] = {}

    for symbol, order_book in state["books"].items():
        markets.setdefault(symbol, {})
        for side in contracts.SIDES:
            for order in order_book[side]:
                key = str(float(order["price"]))
                markets[symbol].setdefault(key, {"BUY": 0, "SELL": 0})[side] += order[
                    "qty"
                ]

    return {
        "markets": markets,
        "trade_log": state["trade_log"],
        "last_prices": state["last_prices"],
    }


def apply_trades_to_state(state, trades):
    state["trade_log"].extend(trades)
    for trade in trades:
        state["last_prices"][trade["symbol"]] = trade["price"]
    pass
