from polygon import RESTClient
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
import numpy as np

import pandas_market_calendars as mcal
from loguru import logger

pk = os.getenv('POLYGON_API_KEY')

client = RESTClient(pk)



def fetch_full_trading_days(start_date, end_date, market='NYSE'):
    # Get the calendar for the specified market
    nyse_calendar = mcal.get_calendar(market)

    # Get the full schedule for the specified date range
    full_schedule = nyse_calendar.schedule(start_date=start_date, end_date=end_date)

    # Filter for full trading days, assuming NYSE standard hours are 9:30 to 16:00 in its local time
    full_days = full_schedule[
        (full_schedule.market_open.dt.tz_convert('America/New_York').dt.time == pd.Timestamp('09:30:00').time()) &
        (full_schedule.market_close.dt.tz_convert('America/New_York').dt.time == pd.Timestamp('16:00:00').time())
    ]

    return full_days.index.date

def is_full_trading_day(row):
        return (row['market_open'].tz_localize(None).time() == market_open_time.time() and
                row['market_close'].tz_localize(None).time() == market_close_time.time())

@logger.catch
def polygonprocess(ticker, start_date, end_date, freq="second", do_log=True, market='NYSE', nocovs = True):
    if market == 'NYSE':
        good_dates = set(fetch_full_trading_days(start_date, end_date, market='NYSE'))
    else:
        good_dates = None

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    datalist = []

    while start_date <= end_date:

        if good_dates is not None and start_date.date() not in good_dates:
            start_date += relativedelta(days=1)
            continue
        logger.info(start_date)

        start_str = start_date.strftime('%Y-%m-%d')
        end_str = (start_date + relativedelta(days=1)).strftime('%Y-%m-%d')

        try:
            bars = client.get_aggs(ticker=ticker, multiplier=1, timespan=freq, from_=start_str, to=end_str, limit=50000)
            df = pd.DataFrame(bars)
            datalist.append(df)
            start_date += relativedelta(days=1)
        except:
            start_date += relativedelta(days=1)

    datadf = pd.concat(datalist).drop_duplicates()
    datadf.timestamp = pd.to_datetime(datadf.timestamp, unit='ms', utc=True)
    datadf.timestamp = datadf.timestamp.dt.tz_convert('America/New_York')
    datadf = datadf.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})
    datadf.set_index('timestamp', inplace=True)

    dflist = []
    for d, df in datadf.groupby(datadf.index.date):
        tmp = df.resample('1s').ffill()
        dflist.append(tmp)
    newdata = pd.concat(dflist)

    if do_log:
        newdata[newdata.select_dtypes(include='number').columns] = newdata.select_dtypes(include='number').applymap(np.log)
        #newdata['Close'] = np.log(newdata['Close'])

    # Filter records to only include those between 10:00 and 16:00 NY time, after ffill
    if freq is not 'day':
        newdata = newdata.between_time('10:00', '16:00')

    # Handle potential duplicates
    if newdata.index.duplicated().any():
        newdata = newdata.groupby(newdata.index).last()

    if nocovs:
        return newdata[['Close']]
    else:
        return newdata
    

    
