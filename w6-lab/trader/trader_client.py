import common.contracts
from exchange import exchange


def create_trader(team_name, cash, shares):
    return {"team": team_name, "cash": cash, "shares": shares, "orders": {}}


def build_order(team, side, symbol, price, qty):
    return common.contracts.make_order(team, side, symbol, price, qty)
    return {}  # could call common.make_order


def submit_order(exchange_state, trader_state, order):
    # TODO: discard invalid?
    trader_state["orders"].setdefault(order["symbol"], list()).append(order.copy())
    trades = exchange.place_order(exchange_state, order)

    # ???
    return trades  # trades


def handle_fills(trader_state, trades):
    # BUG #0 was due to trader_state's orders being the same orders from the
    # global state, so they were already culled as necessary, I hate python and
    # everything references...
    for trade in trades:
        trade_qty = trade["qty"]
        for order in trader_state["orders"][trade["symbol"]]:
            if trade["price"] == order["price"]:
                qty = min(trade_qty, order["qty"])
                trade_qty -= qty
                order["qty"] -= qty
            pass

    pass


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
