# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 18:39:49 2021

@author: Sudeep
"""


import logging
#from kiteconnect import KiteConnect
import pandas as pd
import yfinance as yf
import time


def fetchOHLC(ticker,interval,duration):
    logging.info('starting fetchOHLC for.....'+ticker)
    try:
        """extracts historical data and outputs in the form of dataframe"""
        msft = yf.Ticker(ticker)
        data = pd.DataFrame(msft.history(period=duration, interval=interval))
        """kite api code"""
        # instrument = instrumentLookup(instrument_df,ticker)
        # data = pd.DataFrame(kite.historical_data(instrument,dt.date.today()-dt.timedelta(duration), dt.date.today(),interval))
        # data.set_index("date",inplace=True)
        newdata = data.rename(columns={'Open': 'open','High':'high','Low': 'low','Close':'close'})
    except Exception as e:
        logging.exception("Exception occurred", exc_info=True)
    logging.info('end fetchOHLC for.....'+ticker)
    
    return newdata
def sl_price(ohlc):
    """function to calculate stop loss based on supertrends"""
    st = ohlc.iloc[-1,[-3,-2,-1]]
    if st.min() > ohlc["close"][-1]:
        sl = (0.6*st.sort_values(ascending = True)[0]) + (0.4*st.sort_values(ascending = True)[1])
    elif st.max() < ohlc["close"][-1]:
        sl = (0.6*st.sort_values(ascending = False)[0]) + (0.4*st.sort_values(ascending = False)[1])
    else:
        sl = st.mean()
    return round(sl,1)


def placeSLOrder(symbol,buy_sell,quantity,sl_price):
    logging.info('starting method placeSLOrder for..... '+symbol+ ', NSE,'+str(quantity)+', Market Order, MIS , Regular, '+str(sl_price))    
    # Place an intraday stop loss order on NSE - handles market orders converted to limit orders
    if buy_sell == "buy":
        # t_type=kite.TRANSACTION_TYPE_BUY
        # t_type_sl=kite.TRANSACTION_TYPE_SELL
        t_type="BUY"
        t_type_sl="SELL"
    elif buy_sell == "sell":
        # t_type=kite.TRANSACTION_TYPE_SELL
        # t_type_sl=kite.TRANSACTION_TYPE_BUY
        t_type="SELL"
        t_type_sl="BUY"
    # market_order = kite.place_order(tradingsymbol=symbol,
    #                 exchange=kite.EXCHANGE_NSE,
    #                 transaction_type=t_type,
    #                 quantity=quantity,
    #                 order_type=kite.ORDER_TYPE_MARKET,
    #                 product=kite.PRODUCT_MIS,
    #                 variety=kite.VARIETY_REGULAR)
    data = [
        (symbol, "NSE", t_type,quantity,"Market Order","MIS","Regular")        
    ]
    #print("place Order for..... "+symbol+ ", NSE,"+ str(t_type,quantity)+", Market Order, MIS , Regular ")
    # a = 0
    # while a < 10:
    #     try:
    #         order_list = kite.orders()
    #         break
    #     except:
    #         print("can't get orders..retrying")
    #         a+=1
    # for order in order_list:
    #     if order["order_id"]==market_order:
    #         if order["status"]=="COMPLETE":
    #             kite.place_order(tradingsymbol=symbol,
    #                             exchange=kite.EXCHANGE_NSE,
    #                             transaction_type=t_type_sl,
    #                             quantity=quantity,
    #                             order_type=kite.ORDER_TYPE_SL,
    #                             price=sl_price,
    #                             trigger_price = sl_price,
    #                             product=kite.PRODUCT_MIS,
    #                             variety=kite.VARIETY_REGULAR)
    #         else:
    #             kite.cancel_order(order_id=market_order,variety=kite.VARIETY_REGULAR)
    time.sleep(60)
    data.append([
        (symbol, "NSE", t_type,quantity,"SL Order","MIS","Regular",sl_price)        
    ])
    #print("placeSLOrder for..... "+symbol+ ", NSE,"+ str(t_type,quantity)+", Market Order, MIS , Regular, "+str(sl_price))
    logging.info('ending method placeSLOrder for..... '+symbol+ ', NSE,'+ t_type+', '+str(quantity)+', Market Order, MIS , Regular, '+str(sl_price))    
    return data

# def ModifyOrder(order_id,price):    
#     # Modify order given order id
#     kite.modify_order(order_id=order_id,
#                     price=price,
#                     trigger_price=price,
#                     order_type=kite.ORDER_TYPE_SL,
#                     variety=kite.VARIETY_REGULAR)  

