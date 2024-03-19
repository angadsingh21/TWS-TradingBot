from ib_insync import IB, Index, Option

class SPXOptionsData:
    def __init__(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7496, clientId=888)
        # util.startLoop()  # Uncomment for notebooks

    def connect_and_fetch_data(self):
        self.ib.qualifyContracts(Index('SPX', 'CBOE'))
        self.ib.reqMarketDataType(3)  # Request market data

        # Fetch S&P 500 data
        ticker = self.ib.reqTickers(Index('SPX', 'CBOE'))[0]
        self.spx_value = ticker.marketPrice()

        # Fetch option chains
        self.chains = self.ib.reqSecDefOptParams('SPX', '', 'IND', ticker.contract.conId)

    def create_option_contracts(self):
        current_date = int(datetime.now().strftime("%Y%m%d"))
        expiration = current_date + 1

        chain = next(c for c in self.chains if c.tradingClass == 'SPXW' and c.exchange == 'SMART')
        otm_strikes = [strike for strike in chain.strikes if strike % 1 == 0]

        put_strikes = [strike for strike in otm_strikes if strike < self.spx_value and strike > self.spx_value - 130]
        call_strikes = [strike for strike in otm_strikes if strike > self.spx_value and strike < self.spx_value + 130]

        self.put_contracts = [Option('SPX', expiration, strike, 'P', 'SMART', tradingClass='SPXW') for strike in put_strikes]
        self.call_contracts = [Option('SPX', expiration, strike, 'C', 'SMART', tradingClass='SPXW') for strike in call_strikes]

if __name__ == '__main__':

    options_data = SPXOptionsData()

    options_data.connect_and_fetch_data()

    options_data.create_option_contracts()











util.startLoop()

ib = IB()
ib.connect('127.0.0.1', 7496, clientId = 888)

spx = Index('SPX', 'CBOE')
ib.qualifyContracts(spx)

ib.reqMarketDataType(3) # actual data delayed by 15 mins

[ticker] = ib.reqTickers(spx)

spxValue = ticker.marketPrice()

chains = ib.reqSecDefOptParams(spx.symbol, '', spx.secType, spx.conId) # fetch entire options chain

# Get current date
current_date = int(datetime.now().strftime("%Y%m%d"))

current_date += 1

print(current_date)

chain = next(c for c in chains if c.tradingClass == 'SPXW' and c.exchange == 'SMART')

# get otm strikes only
put_strikes = [strike for strike in chain.strikes
        if strike % 1 == 0
        and strike < spxValue and strike > spxValue - 130]

call_strikes = [strike for strike in chain.strikes
        if strike % 1 == 0
        and strike > spxValue and strike < spxValue + 130]

expiration = current_date

put_contracts = [Option('SPX', expiration, strike, 'P', 'SMART', tradingClass='SPXW')
        for strike in put_strikes]

call_contracts = [Option('SPX', expiration, strike, 'C', 'SMART', tradingClass='SPXW')
        for strike in call_strikes]

put_contracts = ib.qualifyContracts(*put_contracts)
call_contracts = ib.qualifyContracts(*call_contracts)

put_tickers = ib.reqTickers(*put_contracts)
call_tickers = ib.reqTickers(*call_contracts)