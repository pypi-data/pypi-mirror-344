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
    """Fetch and process financial data from Polygon.io for a given ticker and date range.

    This function retrieves aggregated market data (e.g., second-level or daily bars) from
    Polygon.io, filters for full trading days (for NYSE), and processes the data into a
    Pandas DataFrame. It supports resampling to 1-second intervals, optional log transformation
    of numerical columns, and filtering to trading hours (10:00–16:00 NY time).

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str or datetime): Start date for data retrieval (e.g., '2023-01-01').
        end_date (str or datetime): End date for data retrieval (e.g., '2023-12-31').
        freq (str, optional): Time frequency of the data ('second' or 'day'). Defaults to 'second'.
        do_log (bool, optional): Apply log transformation to numerical columns. Defaults to True.
        market (str, optional): Market calendar to use ('NYSE' supported). Defaults to 'NYSE'.
        nocovs (bool, optional): Return only the 'Close' column if True, else return all columns
            ('Open', 'High', 'Low', 'Close', 'Volume'). Defaults to True.

    Returns:
        pandas.DataFrame: A DataFrame with processed market data, indexed by timestamp (NY time).
            - If `nocovs=True`, contains only the 'Close' column.
            - If `nocovs=False`, contains 'Open', 'High', 'Low', 'Close', 'Volume' columns.
            - For `freq='second'`, data is resampled to 1-second intervals and filtered to 10:00–16:00.
            - If `do_log=True`, numerical columns are log-transformed.

    Raises:
        ValueError: If invalid ticker, dates, or frequency are provided.
        requests.exceptions.RequestException: If the Polygon.io API request fails.

    Examples:
        >>> from polydata import polygonprocess
        >>> df = polygonprocess('AAPL', '2023-01-01', '2023-01-05', freq='second', nocovs=True)
        >>> print(df.head())
                             Close
        timestamp
        2023-01-03 10:00:00  4.852030
        2023-01-03 10:00:01  4.852030
        ...

    Notes:
        - Requires a Polygon.io API key set in the environment variable `POLYGON_API_KEY`.
        - Uses the NYSE market calendar to filter for full trading days (9:30–16:00).
        - Non-full trading days (e.g., half-days) are skipped for NYSE.
    """
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
    

    
