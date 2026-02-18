# replace buy/sell with order placement
# build orderbook
# append orders
# print orderbook

import json

from table import Table

traders = {
    "TeamA": {"cash": 1_000_000.0, "shares": 1000},
    "TeamB": {"cash": 1_000_000.0, "shares": 1000},
    "a": {"cash": 1_000_000.0, "shares": 1000},
    "b": {"cash": 1_000_000.0, "shares": 1000},
}

order_book = {'buy': [], 'sell': []}

def best_buy_index(buy_orders):
    if len(buy_orders) == 0:
        return None

    best_i = 0
    for i in range(1, len(buy_orders)):
        if buy_orders[i]['price'] > buy_orders[best_i]['price']:
            best_i = i

    return best_i

def best_sell_index(sell_orders):
    if len(sell_orders) == 0:
        return None

    best_i = 0
    for i in range(1, len(sell_orders)):
        if sell_orders[i]['price'] < sell_orders[best_i]['price']:
            best_i = i

    return best_i

def show_market():
    prices: dict[str, dict[str, int]] = {}

    for order in order_book['buy']:
        key = str(order['price'])
        prices.setdefault(key, {'buy': 0, 'sell': 0})['buy'] += order['qty']

    for order in order_book['sell']:
        key = str(order['price'])
        prices.setdefault(key, {'buy': 0, 'sell': 0})['sell'] += order['qty']


    # return qty for price on side, or empty string if qty == 0; cells look nicer empty
    def get_qty(key, side):
      return prices[str(key)][side] if prices[str(key)][side] != 0 else ""

    # ASCII example
    # +----------+----------+----------+
    # |   Bids   |  Price   |   Asks   |
    # +----------+----------+----------+
    # |      qty |    price |      qty |
    # +----------+----------+----------+
    # |      qty |    price |      qty |
    # +----------+----------+----------+

    # TTY example
    # ┌──────────┬──────────┬──────────┐
    # │   Bids   │  Price   │   Asks   │
    # ├──────────┼──────────┼──────────┤
    # │          │    12.00 │      400 │
    # ├──────────┼──────────┼──────────┤
    # │      500 │    11.00 │          │
    # ├──────────┼──────────┼──────────┤
    # │      100 │    10.00 │          │
    # └──────────┴──────────┴──────────┘

    COLOR_BID = '\033[30;34;1m' # fg: black; bg: blue; bold
    COLOR_ASK = '\033[30;31;1m' # fg: black; bg: red; bold
    COLOR_RST = '\033[0m'

    table = Table("Orderbook")

    table.add_val("Bids")
    table.add_val("Price")
    table.add_val("Asks")
    table.finish_row()

    for key in sorted(map(lambda x: float(x), prices.keys()), reverse=True):
        # |  bid_qty |    price |  ask_qty |
        table.add_val(get_qty(key, 'buy'), color=COLOR_BID)
        table.add_val(key, '.2f')
        table.add_val(get_qty(key, 'sell'), color=COLOR_ASK)
        table.finish_row()

    table.print()


def show_traders():
    table = Table("Traders")

    table.add_val("Team")
    table.add_val("Cash")
    table.add_val("Shares")
    table.finish_row()

    for team, trader in traders.items():
        table.add_val(team)
        table.add_val(trader['cash'], '.2f')
        table.add_val(trader['shares'])
        table.finish_row()

    table.print()


def show_trades(trades):
    table = Table("Trades")
    table.add_val("Buyer")
    table.add_val("Seller")
    table.add_val("Quantity")
    table.add_val("Price")
    table.finish_row()

    for trade in trades:
        table.add_val(trade['buyer'])
        table.add_val(trade['seller'])
        table.add_val(trade['qty'])
        table.add_val(trade['price'], '.2f')
        table.finish_row()

    table.print()

def process_input():
    print("\nEnter order info (no spaces) Ex: TeamA,buy,5,100")
    order_data = input("Order information: ")
    order_data = order_data.split(',')
    return order_data

def place_order(team, side, price, qty):
    global order_book

    order = {'team': team, 'price': float(price), 'qty': int(qty)}

    order_book[side].append(order)

def match_orders():
    trades = []
    while True:
        bi = best_buy_index(order_book['buy'])
        si = best_sell_index(order_book['sell'])

        if bi is None or si is None:
            break;

        print(bi, si)

        buy = order_book['buy'][bi]
        sell = order_book['sell'][si]

        if buy['price'] < sell['price']:
            break;

        trade_qty = min(buy['qty'], sell['qty'])

        trade_price = sell['price'] # thems the breaks, sellers

        buyer = buy['team']
        seller = sell['team']

        trade_cost = trade_price * trade_qty

        if traders[buyer]['cash'] < trade_cost:
            print("Buyer: not enough cash")
            order_book['buy'].pop(bi)
            continue

        if traders[seller]['shares'] < trade_qty:
            print("Seller: not enough shares")
            order_book['sell'].pop(si)
            continue

        traders[buyer]['cash'] -= trade_cost;
        traders[buyer]['shares'] += trade_qty;

        traders[seller]['cash'] -= trade_cost;
        traders[seller]['shares'] -= trade_qty;

        trades.append({
            'buyer': buyer,
            'seller': seller,
            'qty': trade_qty,
            'price': trade_price,
        })

        buy['qty'] -= trade_qty
        sell['qty'] -= trade_qty

        if buy['qty'] <= 0:
            order_book['buy'].pop(bi)
        else:
            order_book['buy'][bi] = buy

        if sell['qty'] <= 0:
            order_book['sell'].pop(si)
        else:
            order_book['sell'][si] = sell


    return trades

while True:
    #print(json.dumps(traders, indent=2))
    show_traders()
    show_market()
    team, side, price, qty = process_input()
    place_order(team, side, price, qty)
    trades = match_orders()
    if len(trades) != 0:
        show_trades(trades)
