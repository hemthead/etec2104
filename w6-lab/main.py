from exchange import exchange
from trader import strategy, trader_client


def run_simulation(num_ticks=50):
    for step in range(num_ticks):
        print(f"Simulation step {step}")
        snapshot = exchange.get_market_snapshot(state)
        order = strategy.decide_order(trader, snapshot)
        trades = exchange.place_order(state, order)
        trader_client.handle_fills(trader, trades)
        # update PnL
        # Log status
        # periodically save state
    print("Simulation finished")


def main():
    run_simulation(num_ticks=50)


if __name__ == "__main__":
    main()
