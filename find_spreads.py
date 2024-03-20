import pandas as pd

from sessions import insync_session
from models import spreads, contracts

def get_data(width, entry_credit, max_call_spreads, max_put_spreads):
    
    options_data = insync_session.SPXOptionsData()
    spr_obj = spreads.Spreads()
    con_obj = contracts.Contracts()

    put_tickers, call_tickers = options_data.get_strikes()

    SC, LC = spr_obj.findCallSpread(
        call_tickers, width, entry_credit, max_call_spreads
    )

    SP, LP = spr_obj.findPutSpread(
        put_tickers, width, entry_credit, max_put_spreads
    )

    call_watchlist = con_obj.create_watchlist(SC, LC)
    put_watchlist = con_obj.create_watchlist(SP, LP)

    return call_watchlist, put_watchlist, options_data.expiration


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

    width = int(width/5 - 1)

    call_watchlist, put_watchlist, contractDate = get_data(
        width, entry_credit, max_call_spreads, max_put_spreads
    )

    print("\n\n", contractDate)

    display_data(call_watchlist, put_watchlist)


if __name__ == "__main__":
    main()