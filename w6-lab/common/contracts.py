SYMBOLS = ["BEAR", "FROG", "LZRD"]
SIDES = ("BUY", "SELL")


def make_order(team, side, symbol, price, qty):
    # copy code here
    return {
        "team": team,
        "side": side,
        "symbol": symbol,
        "price": price,
        "qty": qty,
    }


def make_trade(buyer, seller, symbol, price, qty):
    # copy code here
    return {
        "buyer": buyer,
        "seller": seller,
        "symbol": symbol,
        "price": price,
        "qty": qty,
    }
