from sessions import insync_session
from models import spreads

options_data = SPXOptionsData()
spreads = Spreads()

put_tickers, call_tickers = options_data.get_strikes()

SC, LC = spreads.findCallSpread(call_tickers, width, entry_credit, nos)
SP, LP = spreads.findPutSpread(put_tickers, width, entry_credit, nos)