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

    trader_state["cash"] -= order["price"] * order["qty"]

    if order["side"] == "SELL":
        trader_state["symbols"][order["symbol"]]["shares"] -= order["qty"]

    trader_state["symbols"].setdefault(
        order["symbol"], {"shares": 0, "orders": [order.copy()]}
    )
    trades = exchange.place_order(exchange_state, order)

    # ???
    return trades  # trades


def handle_fills(trader_state, trades):
    # BUG #0 was due to trader_state's orders being the same orders from the
    # global state, so they were already culled as necessary, I hate python and
    # everything references...
    for trade in trades:
        cash_diff = trade["qty"] * trade["price"]
        if trade["buyer"] == trader_state["team"]:
            cash_diff = -cash_diff
            trader_state["symbols"][trade["symbol"]]["shares"] += trade["qty"]

        trader_state["cash"] += cash_diff

        trade_qty = trade["qty"]
        for order in trader_state["symbols"][trade["symbol"]]["orders"]:
            if trade["price"] == order["price"]:
                qty = min(trade_qty, order["qty"])
                trade_qty -= qty
                order["qty"] -= qty


def mark_to_market(trader_state, market_snapshot):
    # calculate actual or realized pnl
    money_in = 0
    money_out = 0

    last_prices = market_snapshot["last_prices"]
    for symbol in last_prices.keys():
        qty_in = 0
        orders = trader_state["orders"][symbol]

        for order in orders:
            qty_in += order["qty"]
            money_in += order["price"] * order["qty"]

        money_out += qty_in * last_prices[symbol]

    # sure, that sounds right enough
    return money_out - money_in
    return 0.0
