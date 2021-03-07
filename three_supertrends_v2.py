# -*- coding: utf-8 -*-

import logging
#from kiteconnect import KiteConnect
from datetime import date
import os
import datetime as dt
import pandas as pd
import numpy as np
import time
import yfinance as yf
import csv

import TradingAPI

# cwd = os.chdir("D:\\Udemy\\Zerodha KiteConnect API\\1_account_authorization")

# #generate trading session
# access_token = open("access_token.txt",'r').read()
# key_secret = open("api_key.txt",'r').read().split()
# kite = KiteConnect(api_key=key_secret[0])
# kite.set_access_token(access_token)


# #get dump of all NSE instruments
# instrument_dump = kite.instruments("NSE")
# instrument_df = pd.DataFrame(instrument_dump)


# def instrumentLookup(instrument_df,symbol):
#     """Looks up instrument token for a given script from instrument dump"""
#     try:
#         return instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]
#     except:
#         return -1



def atr(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['high']-df['low'])
    df['H-PC']=abs(df['high']-df['close'].shift(1))
    df['L-PC']=abs(df['low']-df['close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=n,min_periods=n).mean()
    return df['ATR']


def supertrend(DF,n,m):
    logging.info('starting method supertrend for..... ATR :'+ str(n) +', multiplier :' + str(m))
    """function to calculate Supertrend given historical candle data
        n = n day ATR - usually 7 day ATR is used
        m = multiplier - usually 2 or 3 is used"""
    df = DF.copy()
    df['ATR'] = atr(df,n)
    df["B-U"]=((df['high']+df['low'])/2) + m*df['ATR'] 
    df["B-L"]=((df['high']+df['low'])/2) - m*df['ATR']
    df["U-B"]=df["B-U"]
    df["L-B"]=df["B-L"]
    ind = df.index
    for i in range(n,len(df)):
        if df['close'][i-1]<=df['U-B'][i-1]:
            df.loc[ind[i],'U-B']=min(df['B-U'][i],df['U-B'][i-1])
        else:
            df.loc[ind[i],'U-B']=df['B-U'][i]    
    for i in range(n,len(df)):
        if df['close'][i-1]>=df['L-B'][i-1]:
            df.loc[ind[i],'L-B']=max(df['B-L'][i],df['L-B'][i-1])
        else:
            df.loc[ind[i],'L-B']=df['B-L'][i]  
    df['Strend']=np.nan
    for test in range(n,len(df)):
        if df['close'][test-1]<=df['U-B'][test-1] and df['close'][test]>df['U-B'][test]:
            df.loc[ind[test],'Strend']=df['L-B'][test]
            break
        if df['close'][test-1]>=df['L-B'][test-1] and df['close'][test]<df['L-B'][test]:
            df.loc[ind[test],'Strend']=df['U-B'][test]
            break
    for i in range(test+1,len(df)):
        if df['Strend'][i-1]==df['U-B'][i-1] and df['close'][i]<=df['U-B'][i]:
            df.loc[ind[i],'Strend']=df['U-B'][i]
        elif  df['Strend'][i-1]==df['U-B'][i-1] and df['close'][i]>=df['U-B'][i]:
            df.loc[ind[i],'Strend']=df['L-B'][i]
        elif df['Strend'][i-1]==df['L-B'][i-1] and df['close'][i]>=df['L-B'][i]:
            df.loc[ind[i],'Strend']=df['L-B'][i]
        elif df['Strend'][i-1]==df['L-B'][i-1] and df['close'][i]<=df['L-B'][i]:
            df.loc[ind[i],'Strend']=df['U-B'][i]
    logging.info('ending method supertrend for..... ATR:'+str(n) +', multiplier:' + str(m))
    return df['Strend']


def st_dir_refresh(ohlc,ticker,st_dir):
    logging.info('starting method st_dir_refresh for.....'+ticker)
    """function to check for supertrend reversal"""
    #global st_dir
    count = ohlc["st1"].count()
    if ohlc["st1"][count-1] > ohlc["close"][count-1] and ohlc["st1"][count-2] < ohlc["close"][count-2]:
        st_dir[ticker][0] = "red"
    if ohlc["st2"][count-1] > ohlc["close"][count-1] and ohlc["st2"][count-2] < ohlc["close"][count-2]:
        st_dir[ticker][1] = "red"
    if ohlc["st3"][count-1] > ohlc["close"][count-1] and ohlc["st3"][count-2] < ohlc["close"][count-2]:
        st_dir[ticker][2] = "red"
    if ohlc["st1"][count-1] < ohlc["close"][count-1] and ohlc["st1"][count-2] > ohlc["close"][count-2]:
        st_dir[ticker][0] = "green"
    if ohlc["st2"][count-1] < ohlc["close"][count-1] and ohlc["st2"][count-2] > ohlc["close"][count-2]:
        st_dir[ticker][1] = "green"
    if ohlc["st3"][count-1] < ohlc["close"][count-1] and ohlc["st3"][count-2] > ohlc["close"][count-2]:
        st_dir[ticker][2] = "green"
    logging.info('ending method st_dir_refresh for.....'+ticker)

