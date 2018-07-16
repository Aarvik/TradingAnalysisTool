'''
Netfonds import 5 days of intraday data
'''

import numpy as np
import pandas as p
from pandas.tseries.offsets import *
import datetime as dt
import matplotlib.pyplot as plt
size = (14,10)
import seaborn as sns
sns.set_style('whitegrid')

from pprint import pprint as pp
import time
# ================================================================== #
# timer start #
t0 = time.clock() 

# ================================================ #
# functions
# ~~~~~~~~~~~~~~~~~~

now   = dt.date.today()
year  = str(now.year)
m     = str(now.month)
month = '0'+m

day_5 = now - 5 * BDay()
day_4 = now - 4 * BDay()
day_3 = now - 3 * BDay()
day_2 = now - 2 * BDay()
day_1 = now - 1 * BDay()

days  = [ day_1.day, day_2.day, day_3.day, day_4.day, day_5.day ]
days  = [ str(d) for d in days ]

def netfonds_p( symbol ):
    url_posdump  = r'http://www.netfonds.no/quotes/posdump.php?date=%s%s%s&paper=%s.%s&csv_format=csv'

    sym_posdump  = p.DataFrame()
    cols_posdump = [ 'bid', 'bdepth', 'bdeptht', 'offer', 'odepth', 'odeptht' ]

    # ~~~~~~~~~~~~~~~~~~
    for day in days:
        try:
            sym_posdump = sym_posdump.append( p.read_csv( url_posdump % ( year, month, day, symbol, exchange_sym ), index_col=0, header=0, parse_dates=True ) )   
        except Exception as e:
            print( "{} posdump not found".format( symbol ) )
    sym_posdump.columns = cols_posdump
    # ~~~~~~~~~~~~~~~~~~
    return sym_posdump

def netfonds_t( symbol ):
    url_tdump = r'http://www.netfonds.no/quotes/tradedump.php?date=%s%s%s&paper=%s.%s&csv_format=csv'
    sym_tdump = p.DataFrame()

    # ~~~~~~~~~~~~~~~~~~
    for day in days:
        try:
            sym_tdump = sym_tdump.append( p.read_csv( url_tdump % ( year, month, day, symbol, exchange_sym ),
                        index_col=0, header=0, parse_dates=True ) )
        except Exception as e:
            print( "{} tdump not found".format( symbol ) )
    # ~~~~~~~~~~~~~~~~~~
    return sym_tdump

def resample( data ):
    dat       = data.resample( rule='1min', how='mean').dropna()
    dat.index = dat.index.tz_localize('UTC').tz_convert('US/Eastern')
    dat       = dat.fillna(method='ffill')
    return dat

def trading_start(d):
    mkt_open = dt.datetime( int(year), int(month), int(d), 9, 30 )
    return mkt_open

def trading_end(d):
    mkt_close = dt.datetime( int(year), int(month), int(d), 16, 00 )
    return mkt_close

def trading_hours(data):
    test = []
    for d in days:
        dat = data[ ( data.index > trading_start(d) ) & ( data.index < trading_end(d) ) ]
        test.append( dat )
    return test
    
# ================================================ #
# ticker/data #
# need to know exchange symbol
# N = NYSE
# O = Nasdaq
# A = Amex # common for ETFs
# ~~~~~~~~~~~~~~~~~~
ticker       = 'NKE'
exchange_sym = 'N'

# ~~~~~~~~~~~~~~~~~~
# resample irregular tick data
pos = resample( netfonds_p( ticker ) )
t   = resample( netfonds_t( ticker ).dropna(axis=1) )

# ~~~~~~~~~~~~~~~~~~
# trading hours only
pos_rth = trading_hours( pos )
t_rth   = trading_hours( t )

pos_trading_days = [ pos_rth[0],pos_rth[1],pos_rth[2],pos_rth[3],pos_rth[4] ]
t_trading_days   = [ t_rth[0],t_rth[1],t_rth[2],t_rth[3],t_rth[4] ]

pos_rth = p.concat( pos_trading_days,ignore_index=True )
t_rth   = p.concat( t_trading_days, ignore_index=True )

# ================================================ #
# sample plots

pos_rth[['bid','bdeptht','offer','odeptht']].plot( color='blue', figsize=size, subplots=True )
plt.legend( loc='upper right' )
plt.suptitle('{} bid/offer data'.format(ticker), size=18 )
plt.show()

t_rth.plot( color='blue', figsize=size, subplots=True )
plt.legend( loc='upper right' )
plt.suptitle('{} price/volume data'.format(ticker), size=18 )
plt.show()

# ================================================================== #
# timer looking clean #
secs      = np.round( ( time.clock()  - t0 ), 4 )
time_secs = "{timeSecs} seconds to run".format(timeSecs = secs)
mins      = np.round( ( (  time.clock() ) -  t0 )  / 60, 4 ) 
time_mins = "| {timeMins} minutes to run".format(timeMins = mins)
hours     = np.round( (  time.clock()  -  t0 )  / 60 / 60, 4 ) 
time_hrs  = "| {timeHrs} hours to run".format(timeHrs = hours)
print( time_secs, time_mins, time_hrs )