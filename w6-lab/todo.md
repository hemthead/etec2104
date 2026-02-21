# BUGS

# Archive

## 0 - mismanaged orders
There's a bug where sometimes trades/orders get corrupted. This shows up in FISH on the current seed
at steps 5-6. A trade happens and there's supposed to be 4 sell left, market.match_orders reports
the `bid_rem` and `ask_rem` values correctly after they come back from market.execute_trade...
Somehow these mismanaged orders remain in the orderbook and aren't auto-culled (good thing ig).
