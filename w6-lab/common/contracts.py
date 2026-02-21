from dataclasses import asdict, dataclass
from typing import Literal

type TeamIdent = str
type Side = Literal["BUY"] | Literal["Sell"]
type Symbol = str
type Price = float
type Qty = int

SYMBOLS = ("BEAR", "FROG", "LZRD")
SIDES = ("BUY", "SELL")


@dataclass(slots=True)
class Order:
    team: TeamIdent
    side: Side
    symbol: Symbol
    price: Price
    qty: Qty


def make_order(team, side, symbol, price, qty):
    return asdict(Order(team, side, symbol, price, qty))

    # copy code here
    return {
        "team": team,
        "side": side,
        "symbol": symbol,
        "price": price,
        "qty": qty,
    }


@dataclass(slots=True)
class Trade:
    buyer: TeamIdent
    seller: TeamIdent
    symbol: Symbol
    price: Price
    qty: Qty


def make_trade(buyer, seller, symbol, price, qty):
    return asdict(Trade(buyer, seller, symbol, price, qty))

    # copy code here
    return {
        "buyer": buyer,
        "seller": seller,
        "symbol": symbol,
        "price": price,
        "qty": qty,
    }


@dataclass(slots=True)
class Trader:
    team: TeamIdent
    cash: Price
    markets: dict[Symbol, Market]

    @dataclass(slots=True)
    class Market:
        shares: Qty
        orders: list[Order]


@dataclass(slots=True)
class MarketSnapshot:
    trade_log: list[Trade]
    last_prices: list[Price]
    markets: dict[Symbol, Market]

    type Market = dict[Price, PriceLevel]
    type PriceLevel = dict[Side, Qty]
