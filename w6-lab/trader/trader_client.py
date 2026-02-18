def create_trader(team_name, cash, shares):
    return {}


def build_order(team, side, symbol, price, qty):
    return {}  # could call common.make_order


def submit_order(exchange_state, trader_state, order):
    return []  # trades


def handle_fills(trader_state, trades):
    pass


def mark_to_market(trader_state, market_snapshot):
    # calculate actual or realized pnl
    return 0.0
