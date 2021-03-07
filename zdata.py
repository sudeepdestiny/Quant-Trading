import click
import pickle as pk
import csv
from jugaad_trader import Zerodha
import pandas as pd
import datetime as dt
import logging

# @click.command()
# @click.option("--instrument", "-i", help='Instrument name "NSE:INFY"', type=str)
# @click.option("--from", "-f", "from_", help="from date yyyy-mm-dd")
# @click.option("--to", "-t", help="to date yyyy-mm-dd")
# @click.option("--interval", "-n", default="day", help="Data interval eg. minute, day")
# @click.option("--output", "-o", help="Output file name")

def login():
    kite = Zerodha()
    #kite.set_access_token()        
    kite.load_creds()
    kite.login()
    logging.info("Kite Login details")
    return kite
        

def main(ticker, interval,duration):
    #print(instrument, from_, to, interval, output)
    #ticker="BURGER KING"

    try:
       # login()
        kite = Zerodha()
        kite.set_access_token() 
        #get dump of all NSE instruments
        instrument_dump = kite.instruments("NSE")
        instrument_df = pd.DataFrame(instrument_dump.get("NSE"),columns=["instrument_token", "tradingsymbol", "name", "last_price", "expiry", "strike"])
        #instrument_df.to_csv('output.csv',index=False,header=True)
        instrument = instrument_df[instrument_df['name'].str.contains(ticker, na=False)].tradingsymbol.values[0]
        instrument = "NSE:"+instrument
        
        #instrument = instrumentLookup(instrument_df,ticker)
        #print(instrument_df)
        # with open("instruments.csv", 'w') as fp:
        #     writer = csv.DictWriter(fp, ["date", "open", "high", "low", "close", "volume"])
        #     writer.writeheader()
        #     writer.writerows(instrument_dump.get("NSE"))

        # #instrument = instrumentLookup(instrument_df,ticker)
        

        q = kite.ltp(instrument)
        token = q[instrument]['instrument_token']

        #data = kite.historical_data(token, from_, to, interval)
        data = pd.DataFrame(kite.historical_data(token,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
        return data   
        # with open(output, 'w') as fp:
        #     writer = csv.DictWriter(fp, ["date", "open", "high", "low", "close", "volume"])
        #     writer.writeheader()
        #     writer.writerows(data)
    except Exception as e:
            logging.exception("Exception occurred", exc_info=True)
            print("API error for ticker :",ticker)


# if __name__ == "__main__":
#     main("stock","2020-12-01","2020-12-02","minute")