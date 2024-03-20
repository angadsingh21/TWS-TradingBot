import pandas as pd

class Contracts:

    def create_watchlist(self, shortContract, longContract):

        watchlist = pd.DataFrame( columns=["pos", "strike", "bid", "ask", "mid_price", "credit"] )
        
        data = []

        for short_tick, long_tick in zip(shortContract, longContract):

            data.append({
                "pos": "SHORT",
                "strike": short_tick.contract.strike,
                "bid": short_tick.bid,
                "ask": short_tick.ask,
                "mid_price": (short_tick.bid + short_tick.ask) / 2,
                "credit": "-"
            })

            data.append({
                "pos": "LONG",
                "strike": long_tick.contract.strike,
                "bid": long_tick.bid,
                "ask": long_tick.ask,
                "mid_price": (long_tick.bid + long_tick.ask) / 2,
                "credit": "-"
            })

            credit =  (short_tick.bid + abs(short_tick.ask - short_tick.bid) / 2) - (long_tick.bid + abs(long_tick.ask - long_tick.bid) / 2)
            data.append({"pos": "-", "strike": "-", "bid": "-", "ask": "-", "mid_price": "-", "credit": credit})

        watchlist = pd.DataFrame(data)
        return watchlist