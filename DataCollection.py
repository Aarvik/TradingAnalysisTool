# -*- coding: utf-8 -*-

"""
Created on Mon Jul 16 23:14:35 2018

@author: Kristoffer

This file will hold the data collection functions of the project

It also includes a quick way of recieving the tickers off of Oslo Børs.

The URL which we will collect data from is:
https://www.netfonds.no/quotes/paperhistory.php?paper=TICKER.OSE&csv_format=csv

This will return the date, the ticker, the exchange, open value, high value, low value, close value, volume and value.
Ranging from trading start for the ticker to current year. 

At the moment it saves it as a .csv file.

"""

#Todo 
# Create the deltadatacollection function
# Deliver the data to a DB directly

import numpy as np
import pandas as pd
import requests as r
import io
import json


def GetOSETickersAndNames():
#I manually cleaned the data. It is probably pretty easy to do it directly but it served my purpose. Check the repo for a ticker-list if you don't want the hassle"""
#TODO - Create an actual parser Parser
    TURL="https://www.oslobors.no/ob/servlets/components?type=table&generators%5B0%5D%5Bsource%5D=feed.ose.quotes.EQUITIES%2BPCC&filter=VOLUME_TOTAL%3En0&view=DELAYED&columns=ITEM_SECTOR%2C+ITEM%2C+LONG_NAME%2C&channel=5571c881cdd34770e386931bddb48f05"
    TickerRaw=pd.read_json(TURL)
    T=TickerRaw.to_csv('TickersAndNames',index=False)
    

def DataCollectionNetFonds(Ticker):
    print("Henter data for " + Ticker)
    a="https://www.netfonds.no/quotes/paperhistory.php?paper="
    b=Ticker
    c=".OSE&csv_format=csv"
    url=a+b+c    
    #url="https://www.netfonds.no/quotes/paperhistory.php?paper=DNB.OSE&csv_format=csv" ####This one works
    s=r.get(url).content
    c=pd.read_csv(io.StringIO(s.decode("ISO-8859-1")))
    stockname="Lagret data for_" + b
    
    #c.to_csv(filename, index=False) OLDCODE
    #print(c) OLDCODE
    print(stockname)
    return (c)
    
def DeltaDataCollectionNetFonds(Ticker, LastDate): #TODO - Use the Lastdate parameter
    print("Henter data for " + Ticker)
    a="https://www.netfonds.no/quotes/paperhistory.php?paper="
    b=Ticker
    c=".OSE&csv_format=csv"
    url=a+b+c    
    #url="https://www.netfonds.no/quotes/paperhistory.php?paper=DNB.OSE&csv_format=csv" ####This one works
    s=r.get(url).content
    c=pd.read_csv(io.StringIO(s.decode("ISO-8859-1")))
    print(c)

def GetHistoricalDataforTickers():
    MyTickerList='D:\Programmering\TradingAnalysisTool\FinalTickersAndNamesMod.xlsx'
    Newdf=pd.DataFrame() #creates an empty dataframe
    tickertable=pd.read_excel(MyTickerList, index_col='id')
    for index, row in tickertable.iterrows():
        Newdf=Newdf.append(DataCollectionNetFonds((row['ticker'])))
    Newdf.to_csv('HistoricDataOSE.csv')
        
            
#So this runs it all. You do not have do anything as long as you have the files. Just remove the comment to run everything.
#GetHistoricalDataforTickers()
