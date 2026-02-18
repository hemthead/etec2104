# STATE
# Price = ?
# Cash = ?
# Inventory = ?
# Orders = ?

type Price = float
price: Price = 100.0

type Trader = dict[str, float | int]

traders: dict[str, Trader] = {
    "TeamA": {"cash": 1000.0, "shares": 0},
    "TeamB": {"cash": 1000.0, "shares": 0},
}

orders = []


def sell(team):
    global price

    if traders[team]["shares"] > 0:
        # take their share and add some cash
        traders[team]["shares"] -= 1
        traders[team]["cash"] += price
        # only one share at each price, decrement to next price level
        price -= 1
    else:
        print("No shares to sell")


def buy(team):
    global price

    # assume qty == 1
    if traders[team]["cash"] >= price:
        # take their cash and add a share
        traders[team]["cash"] -= price
        traders[team]["shares"] += 1
        # only one share at each price, increment to next price level
        price += 1
    else:
        print("Insufficient Funds")


def show_market():
    print("Current price:", price)
    for t in traders.keys():
        print(t, traders[t])


def process_input():
    team = input("What is your team name? ")
    choice = input("(B)uy or (S)ell? ")

    if choice == "B" or choice == "b":
        buy(team)
    if choice == "S" or choice == "s":
        sell(team)


def update_market():
    pass


while True:
    show_market()
    process_input()
    update_market()
