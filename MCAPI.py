import numpy as np # linear algebra
import pandas as pd # pandas for dataframe based data processing and CSV file I/O
import requests # for http requests
from bs4 import BeautifulSoup # for html parsing and scraping
import bs4
import zdata as zd
def findTrendingStocks(limit):
    response = requests.get("https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php", timeout=240)
    soup = BeautifulSoup(response.content, "html.parser")
    table_div = soup.find('div' , attrs={'class':'bsr_table hist_tbl_hm'})
    table = table_div.find('table')
    stocks=[]
    rows = table.findChildren(['tr'])
    for row in rows:
        cells = row.findChildren('td',attrs ={'class':'PR'})    
        for cell in cells:
            spans = cell.findChildren('span',attrs ={'class':'gld13 disin'})
            stocks.append(spans[1].string)
            if(len(stocks) == limit):
                return stocks
            #print("The value in this cell is %s" % spans[1].string)
    return stocks
# stocks = findTrendingStocks(10)
# for stock in stocks:
#     zd.main(stock.upper(),"2020-12-01","2020-12-02","minute","output_"+stock+".csv")
