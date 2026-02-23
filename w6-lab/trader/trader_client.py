from common import contracts
from exchange import exchange


def create_trader(team_name, cash, starting_shares_per):
    trader = {"team": team_name, "cash": cash, "symbols": {}}

    for symbol in contracts.SYMBOLS:
        trader["symbols"].setdefault(
            symbol, {"shares": starting_shares_per, "orders": []}
        )

    return trader


def build_order(team, side, symbol, price, qty):
    return contracts.make_order(team, side, symbol, price, qty)
    return {}  # could call common.make_order


def submit_order(exchange_state, trader_state, order):
    # TODO: discard invalid?

    # assuming order["team"] refers to trader_state

    if order["team"] != trader_state["team"]:
        return None

    if order["side"] == "SELL":
        trader_state["symbols"][order["symbol"]]["shares"] -= order["qty"]
    else:
        trader_state["cash"] -= order["price"] * order["qty"]

    trader_state["symbols"].setdefault(order["symbol"], {"shares": 0, "orders": []})[
        "orders"
    ].append(order.copy())
    trades = exchange.place_order(exchange_state, order)

    # ???
    return trades  # trades


def handle_fills(trader_state, trades):
    # BUG #0 was due to trader_state's orders being the same orders from the
    # global state, so they were already culled as necessary, I hate python and
    # everything references...
    for trade in trades:
        cash_diff = trade["qty"] * trade["price"]

        if trade["seller"] == trader_state["team"]:
            trader_state["cash"] += cash_diff
        elif trade["buyer"] == trader_state["team"]:
            trader_state["symbols"][trade["symbol"]]["shares"] += trade["qty"]

        trade_qty = trade["qty"]
        for order in trader_state["symbols"][trade["symbol"]]["orders"]:
            if trade["price"] == order["price"]:
                qty = min(trade_qty, order["qty"])
                trade_qty -= qty
                order["qty"] -= qty

                if order["qty"] <= 0:
                    trader_state["symbols"][trade["symbol"]]["orders"].remove(order)


def mark_to_market(trader_state, market_snapshot):
    # calculate actual or realized pnl
    money_in = 0
    money_out = 0

    last_prices = market_snapshot["last_prices"]
    for symbol in last_prices.keys():
        qty_in = 0
        orders = trader_state["symbols"][symbol]["orders"]
        last_price = last_prices[symbol]
        if last_price is None:
            last_price = 1

        for order in orders:
            if order["side"] == "BUY":
                money_in += order["price"] * order["qty"]
            else:
                qty_in += order["qty"]

        money_out += qty_in * last_price

    # sure, that sounds right enough
    return money_out - money_in
    return 0.0
