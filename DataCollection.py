# -*- coding: utf-8 -*-

"""
Created on Mon Jul 16 23:14:35 2018

@author: Kristoffer

This file will hold the data collection functions of the project

The URL which we will collect data from is:
https://www.netfonds.no/quotes/paperhistory.php?paper=TICKER.OSE&csv_format=csv

This will return the date, the ticker, the exchange, open value, high value, low value, close value, volume and value.
Ranging from trading start for the ticker to current year. 

"""

#Todo 
#1. Import ticker list first
#2. Make it dynamic based on date to capture delta data

import numpy as np
import pandas as p
import requests as r
import io


def GetOSETickets():
    #TODO
    """
    Parse resulting JSON from:
    https://www.oslobors.no/ob/servlets/components?type=table&generators%5B0%5D%5Bsource%5D=feed.ose.quotes.EQUITIES%2BPCC&filter=VOLUME_TOTAL%3En0&view=DELAYED&columns=PERIOD%2C+INSTRUMENT_TYPE%2C+TRADE_TIME%2C+ITEM_SECTOR%2C+ITEM%2C+LONG_NAME%2C+BID%2C+ASK%2C+LASTNZ_DIV%2C+CLOSE_LAST_TRADED%2C+CHANGE_PCT_SLACK%2C+TURNOVER_TOTAL%2C+TRADES_COUNT_TOTAL%2C+MARKET_CAP%2C+HAS_LIQUIDITY_PROVIDER%2C+PERIOD%2C+MIC%2C+GICS_CODE_LEVEL_1%2C+TIME%2C+VOLUME_TOTAL&channel=5571c881cdd34770e386931bddb48f05
    """
    


def DataCollectionNetFonds(Ticker): #TODO Use the parameter Lastdate to capture delta data
    print("Henter data for " + Ticker)
    a="https://www.netfonds.no/quotes/paperhistory.php?paper="
    b=Ticker
    c=".OSE&csv_format=csv"
    url=a+b+c    
    #url="https://www.netfonds.no/quotes/paperhistory.php?paper=DNB.OSE&csv_format=csv" ####This one works
    s=r.get(url).content
    c=p.read_csv(io.StringIO(s.decode("ISO-8859-1")))
    print(c)
    


DataCollectionNetFonds("DNB")
