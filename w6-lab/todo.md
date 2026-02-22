# Issues

## 1 - Better strategies
Even strategies like random should take more into account. Ex. random should
take the market on a random-walk, not just randomly make orders. (this is more
fun and more productive).

## 2 - Multiple Orders at Once
Some strategies may want to make multiple orders at once, allow for this.

## 3 - General Data Restructure
There are places where it makes sense to restructure our data. For example, the
trader should have shares on a per-market basis.

# Archive

## 0 - mismanaged orders
There's a bug where sometimes trades/orders get corrupted. This shows up in FISH
on the current seed at steps 5-6. A trade happens and there's supposed to be 4
sell left, market.match_orders reports the `bid_rem` and `ask_rem` values
correctly after they come back from market.execute_trade... Somehow these
mismanaged orders remain in the orderbook and aren't auto-culled (good thing
ig).
