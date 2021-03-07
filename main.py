# -*- coding: utf-8 -*-

import logging
#from kiteconnect import KiteConnect
from datetime import date
import os
import datetime as dt
import pandas as pd
import numpy as np
import time
#import yfinance as yf
import csv

import TradingAPI as ta
import three_supertrends_v2 as st
import MCAPI as ma
import zdata as zd

def main(capital):
    # a,b = 0,0
    # while a < 10:
    #     try:
    #         pos_df = pd.DataFrame(kite.positions()["day"])
    #         break
    #     except:
    #         print("can't extract position data..retrying")
    #         a+=1
    # while b < 10:
    #     try:
    #         ord_df = pd.DataFrame(kite.orders())
    #         break
    #     except:
    #         print("can't extract order data..retrying")
    #         b+=1
    
    #filepath = "D:\\trading\\trading"
    filepath = "/home/ec2-user/trading/trading/trading"
    # logFilePath=filepath+'trading.log'
    logging.basicConfig(filename=filepath+'_'+date.today().strftime("%d_%m_%Y")+'.log',filemode='w', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Started')
    filename = filepath+"_Order_Placed_On_"+date.today().strftime("%d_%m_%Y")+".csv"
    header = ("tradingsymbol", "exchange","transaction_type","quantity","order_type","product","variety","price")

    #login kite
    #kite = zd.login()

    for ticker in tickers:
        logging.info('starting passthrough for.....'+ticker)
        print("starting passthrough for.....",ticker)
        try:
            ohlc = zd.main(ticker.upper(),"5minute",5)
            ohlc["st1"] = st.supertrend(ohlc,7,3)
            ohlc["st2"] = st.supertrend(ohlc,10,3)
            ohlc["st3"] = st.supertrend(ohlc,11,2)
            ohlc = ohlc.dropna()
            st.st_dir_refresh(ohlc,ticker,st_dir)
            #st_dir_refresh(ohlc,"^NSEBANK")
            quantity = int(capital/ohlc["close"][ohlc["st1"].count()-1])
            if st_dir[ticker] == ["green","green","green"]:
                    data = ta.placeSLOrder(ticker,"buy",quantity,ta.sl_price(ohlc))                   
                    writer(header, data, filename, "write")
                     
            if st_dir[ticker] == ["red","red","red"]:
                    data=ta.placeSLOrder(ticker,"sell",quantity,ta.sl_price(ohlc))
                    writer(header, data, filename, "write")
            # if len(pos_df.columns)==0:
            #     if st_dir[ticker] == ["green","green","green"]:
            #         placeSLOrder(ticker,"buy",quantity,sl_price(ohlc))
            #     if st_dir[ticker] == ["red","red","red"]:
            #         placeSLOrder(ticker,"sell",quantity,sl_price(ohlc))
            # if len(pos_df.columns)!=0 and ticker not in pos_df["tradingsymbol"].tolist():
            #     if st_dir[ticker] == ["green","green","green"]:
            #         placeSLOrder(ticker,"buy",quantity,sl_price(ohlc))
            #     if st_dir[ticker] == ["red","red","red"]:
            #         placeSLOrder(ticker,"sell",quantity,sl_price(ohlc))
            # if len(pos_df.columns)!=0 and ticker in pos_df["tradingsymbol"].tolist():
            #     if pos_df[pos_df["tradingsymbol"]==ticker]["quantity"].values[0] == 0:
            #         if st_dir[ticker] == ["green","green","green"]:
            #             placeSLOrder(ticker,"buy",quantity,sl_price(ohlc))
            #         if st_dir[ticker] == ["red","red","red"]:
            #             placeSLOrder(ticker,"sell",quantity,sl_price(ohlc))
            #     if pos_df[pos_df["tradingsymbol"]==ticker]["quantity"].values[0] != 0:
            #         order_id = ord_df.loc[(ord_df['tradingsymbol'] == ticker) & (ord_df['status'].isin(["TRIGGER PENDING","OPEN"]))]["order_id"].values[0]
            #         ModifyOrder(order_id,sl_price(ohlc))
        
        except Exception as e:
            logging.exception("Exception occurred", exc_info=True)
            print("API error for ticker :",ticker)

def writer(header, data, filename, option):
        with open (filename, "w", newline = "") as csvfile:
            if option == "write":

                movies = csv.writer(csvfile)
                movies.writerow(header)
                for x in data:
                    movies.writerow(x)
            elif option == "update":
                writer = csv.DictWriter(csvfile, fieldnames = header)
                writer.writeheader()
                writer.writerows(data)
            else:
                print("Option is not known")
           
#############################################################################################################
#############################################################################################################
tickers = ma.findTrendingStocks(10)

#tickers to track - recommended to use max movers from previous day
capital = 300000 #position size
st_dir = {} #directory to store super trend status for each ticker
for ticker in tickers:
    st_dir[ticker] = ["None","None","None"]    
    
# main(capital)
    
starttime=time.time()
timeout = time.time() + 60*60*1  # 60 seconds times 360 meaning 6 hrs
while time.time() <= timeout:
    try:
        main(capital)
        time.sleep(300 - ((time.time() - starttime) % 300.0))
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()        



