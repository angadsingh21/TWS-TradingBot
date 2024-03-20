import pandas as pd

from ..sessions import insync_session
from models import spreads, contracts

def get_data(width, entry_credit, max_call_spreads, max_put_spreads):
    
    options_data = SPXOptionsData()
    spreads = Spreads()
    contracts = Contracts()

    put_tickers, call_tickers = options_data.get_strikes()

    SC, LC = spreads.find_call_spread(
        call_tickers, width, entry_credit, max_call_spreads
    )

    SP, LP = spreads.find_put_spread(
        put_tickers, width, entry_credit, max_put_spreads
    )

    call_watchlist = contracts.create_watchlist(SC, LC)
    put_watchlist = contracts.create_watchlist(SP, LP)

    return call_watchlist, put_watchlist


def display_data(call_watchlist, put_watchlist):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print("\n========= CALL Watchlist ========")
    print(call_watchlist)

    print("\n========= PUT Watchlist ========")
    print(put_watchlist)


def main():

    width = int(input("Enter the width of the spread (int): "))
    entry_credit = float(input("Enter the entry_credit (float): "))
    max_call_spreads = int(input("Enter the max number of call spreads: "))
    max_put_spreads = int(input("Enter the max number of put spreads: "))

    call_watchlist, put_watchlist = get_data(
        width, entry_credit, max_call_spreads, max_put_spreads
    )

    display_data(call_watchlist, put_watchlist)


if __name__ == "__main__":
    main()