from datetime import datetime

import yfinance as yf
import pandas as pd
import os
import sys

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def get_hist_data(codes):
    df_dict = {}
    for code in codes:
        file_path = code + '_1D.csv'
        ticker = yf.Ticker(code)

        if os.path.isfile(file_path) is True:
            df = pd.read_csv(file_path)

            df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
            df['date'] = pd.to_datetime(df['date'], utc=True)
            df = df.set_index('datetime')
            print(datetime.now(), code, 'successfully read data')
        else:
            df = ticker.history(period='12mo')
            df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
            df = df[df['Volume'] > 0]
            df = df.rename(columns={'Open':'open', 'High':'high', 'Low':'low', 'Close':'close', 'Volume':'volume'})
            df = df.rename_axis('datetime')
            df['date'] = df.index.date
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

            print(datetime.now(), code, 'successfully get data from source.')
            df.to_csv(file_path)

        df_dict[code] = df

    return df_dict

codes = ['AAPL','0700.HK']
df_dict = get_hist_data(codes)
print(df_dict)