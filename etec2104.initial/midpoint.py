def compute_mid():
    if bid > ask:
        print(f"Warning the BID {bid} is greater than the ASK {ask}")

    mid = (ask + bid) / 2.0
    return mid

for i in range(3):
    product = input("Enter product name: ")
    bid = float(input("Enter bid price: "))
    ask = float(input("Enter ask price: "))
    mid = compute_mid()
    print(f"{product} mid-price is {mid:.3f}")

