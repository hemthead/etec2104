import common.contracts


def match_orders(state, symbol):
    order_book = state["books"][symbol]

    trades = []
    while True:
        bid = best_bid(order_book)
        ask = best_ask(order_book)

        if bid is None or ask is None:
            break

        trade, bid_rem, ask_rem = execute_trade(bid, ask)

        if trade is None:
            break

        trades.append(trade)

        remove_filled_orders(order_book)

    return trades  # trades


def best_bid(book):
    orders = book["BUY"]

    if len(orders) == 0:
        return None

    best = orders[0]
    for i in range(0, len(orders)):
        if orders[i]["price"] > best["price"]:
            best = orders[i]

    return best


def best_ask(book):
    orders = book["SELL"]

    if len(orders) == 0:
        return None

    best = orders[0]
    for i in range(0, len(orders)):
        if orders[i]["price"] < best["price"]:
            best = orders[i]

    return best


def insert_order(book, order):
    book[order["side"]].append(order)
    pass


def execute_trade(bid, ask):
    if bid["price"] < ask["price"]:
        return (None, bid["qty"], ask["qty"])

    trade_qty = min(bid["qty"], ask["qty"])

    trade_price = ask["price"]  # thems the breaks, sellers

    buyer = bid["team"]
    seller = ask["team"]

    trade_cost = trade_price * trade_qty

    trade = common.contracts.make_trade(
        buyer, seller, bid["symbol"], trade_price, trade_qty
    )

    bid["qty"] -= trade_qty
    ask["qty"] -= trade_qty

    return (trade, bid["qty"], ask["qty"])
    pass  # return (trade, bid_remaining, ask_remaining)


def remove_filled_orders(book):
    for side in common.contracts.SIDES:
        # iterate backward because pop
        order_i = 0
        while order_i < len(book[side]):
            if book[side][order_i]["qty"] <= 0:
                order_i -= 1
            order_i += 1
    pass
