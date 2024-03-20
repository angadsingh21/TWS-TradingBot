import math

class Spreads:

    def calc_credit(self, contract_tickers, ticker, short_indx):

        long_bid = ticker.bid
        long_ask = ticker.ask

        short_bid = contract_tickers[short_indx].bid
        short_ask = contract_tickers[short_indx].ask
        
        short_mid = short_bid + (short_ask - short_bid) / 2
        long_mid = long_bid + (long_ask - long_bid) / 2

        # short mid price - long mid price = credit collected
        credit = short_mid - long_mid

        return credit
    

    def findCallSpread(self, call_tickers, width, entry_credit, nos):

        indx = 0
        spread_count = 0
        short_call_spread = []
        long_call_spread = []

        for ticker in call_tickers[::-1]:

            indx +=1
            short_indx = len(call_tickers) - ( indx + width + 1 )

            if math.isnan(ticker.bid) or ticker.bid < 0: # ignore long calls with no bids
                continue

            try:
                credit = self.calc_credit(call_tickers, ticker, short_indx)
            
            except Exception as e:
                print(f"Exception: {type(e)}")  # Print exception type
                print(f"Error message: {e}")     # Print exception message
                continue

            if credit >= entry_credit - 0.001:
                
                short_call_spread.append(call_tickers[short_indx])
                long_call_spread.append(ticker)

                spread_count += 1

                if spread_count == nos:
                    return short_call_spread, long_call_spread


    def findPutSpread(self, put_tickers, width, entry_credit, nos):

        indx = -1
        spread_count = 0
        short_put_spread = []
        long_put_spread = []

        for ticker in put_tickers:

            indx +=1
            short_indx = indx + width + 1 

            if math.isnan(ticker.bid) or ticker.bid < 0: # ignore puts with no bids
                continue

            try:
                credit = self.calc_credit(put_tickers, ticker, short_indx)
            
            except Exception as e:
                print(f"Exception: {type(e)}")  # Print exception type
                print(f"Error message: {e}")     # Print exception message
                continue

            if credit >= entry_credit - 0.001:
                
                short_put_spread.append(put_tickers[short_indx])
                long_put_spread.append(ticker)

                spread_count += 1

                if spread_count == nos:
                    return short_put_spread, long_put_spread
