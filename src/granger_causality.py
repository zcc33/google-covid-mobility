import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

def clean_data(df):
    df[mobility] = df[mobility].interpolate(limit=2)
    df[restrictions] = df[restrictions].fillna(method="ffill", limit=7)
    df[virus] = df[virus].interpolate(limit=2)

    for i in range(1,df.shape[0]):
        previous = df["new_confirmed"].iloc[i-1]
        current = df["new_confirmed"].iloc[i]
        if not pd.isnull(previous) and not pd.isnull(current) and current < 0.05*previous:
            df["new_confirmed"].iloc[i] = previous
            
    for i in range(1,df.shape[0]):
        previous = df["cumulative_persons_fully_vaccinated"].iloc[i-1]
        current = df["cumulative_persons_fully_vaccinated"].iloc[i]
        if not pd.isnull(previous) and not pd.isnull(current) and current < 0.05*previous:
            df["cumulative_persons_fully_vaccinated"].iloc[i] = previous

    df[mobility] = df[mobility].rolling(7, center=True).mean()
    df[virus] = df[virus].rolling(7, center=True).mean()

if __name__ == "__main__":
    mobility = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks", "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]
    restrictions = ["school_closing", "workplace_closing", "cancel_public_events","restrictions_on_gatherings", "public_transport_closing", "stay_at_home_requirements", "restrictions_on_internal_movement", "stringency_index"]
    virus = ["new_confirmed", "cumulative_persons_fully_vaccinated"]

    data_key = "US"
    df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{data_key}.csv', parse_dates=["date"], index_col="date")
    df=df[mobility+restrictions+virus]
    clean_data(df)

    date_window = pd.date_range(start = "2020-02-25", end = "2021-06-1")
    df_test=df.loc[date_window,:]
    x = np.diff(df_test["mobility_retail_and_recreation"])[1:]
    y = np.diff(df_test["stringency_index"])[1:]
    data = {"x": x, "y": y}
    data_df = pd.DataFrame(data)
    grangercausalitytests(data_df, maxlag=7)