import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from clean_data import clean_data
from statsmodels.tsa.stattools import grangercausalitytests

"""
  Perform granger causality test on whether stringency_index contains predictive information
  about mobility_retail_and_recreation. Contains option to perform test on differenced data to
  reduce non-stationarity.

  Parameters:
  -----------
  df (DataFrame): cleaned data
  diff (boolean, default True): if true, performs test on differenced data, otherwise uses raw data
  max_lag (int, default 7): max lag to use for granger causality test

  Returns
  -------
  none
  """
def granger_test(df, diff=True, max_lag=7):
    if diff:
        x = np.diff(df["mobility_retail_and_recreation"])[1:]
        y = np.diff(df["stringency_index"])[1:]
        data = {"x": x, "y": y}
        data_df = pd.DataFrame(data)
        grangercausalitytests(data_df, maxlag=7)
    else:
        grangercausalitytests(df[["mobility_retail_and_recreation", "stringency_index"]], maxlag=max_lag)

if __name__ == "__main__":
    #download and clean US dataset
    data_key = "US"
    df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{data_key}.csv', parse_dates=["date"], index_col="date")
    df = clean_data(df)

    #uses data from Feb. 25 2020 to June 1 2021 because no missing data allowed for test
    date_window = pd.date_range(start = "2020-02-25", end = "2021-06-1")
    df_test=df.loc[date_window,:]

    #perform granger causality test
    granger_test(df_test, True, 7)