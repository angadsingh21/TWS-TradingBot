from ib_insync import IB, Index, Option
from datetime import datetime

class SPXOptionsData:
    def __init__(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7496, clientId=888)

    def fetch_SPX(self):

        self.spx = Index('SPX', 'CBOE')
        self.ib.qualifyContracts(self.spx)

        # Fetch S&P 500 data
        self.ib.reqMarketDataType(3) # actual data delayed by 15 mins
        [ticker] = self.ib.reqTickers(self.spx)
        self.spxValue = ticker.marketPrice()

    def get_strikes(self):
        current_date = int(datetime.now().strftime("%Y%m%d"))
        expiration = current_date + 1

        # gen OTM call strikes
        call_strikes = [value for value in range( int( (self.spxValue) // 5 + 1 ) * 5, int(self.spxValue + 135), 5)]
        put_strikes = [value for value in range( int( (self.spxValue) // 5 + 1 ) * 5, int(self.spxValue - 135), -5)]

        put_contracts = [Option('SPX', expiration, strike, 'P', 'SMART', tradingClass='SPXW') for strike in put_strikes]
        call_contracts = [Option('SPX', expiration, strike, 'C', 'SMART', tradingClass='SPXW') for strike in call_strikes]