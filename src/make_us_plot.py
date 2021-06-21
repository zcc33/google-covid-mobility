import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from clean_data import clean_data

"""
Creates plot of overall mobility trends for the US during the COVID outbreak.

Variables are daily time series representing percentage change from baseline (January 2020). Percentage
change is calculated by day of the week. Note the heavy influence of seasonality since baseline was during
winter. Choppiness from day-of-week was smoothed out by taking the 7-day moving average.

Saves image as ../img/us_mobility_all.png
"""

if __name__ == "__main__":
    #download and clean US data
    data_key = "US"
    df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{data_key}.csv', parse_dates=["date"], index_col="date")
    df=clean_data(df)

    #use time window Jan. 1 2020 to June 8 2021
    date_window = pd.date_range(start = "2020-01-01", end = "2021-06-8")
    df_plot=df.loc[date_window,:]

    #plot all mobility variables against time during COVID outbreak
    mobility = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks", "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]
    fig, ax = plt.subplots(figsize=(10,6),dpi=200)
    ax.plot(df_plot.index, df_plot[mobility])
    ax.set_xlabel("")
    ax.set_ylabel("Change (%) from Baseline", fontsize=12)
    ax.set_title("U.S. Mobility Trends since COVID", fontsize = 15)
    ax.legend(["Retail and Recreation","Grocery and Pharmacy", "Parks", "Transit Stations", "Workplaces", "Residential"], fontsize=8, loc = "upper right")
    ax.axvspan(datetime.date(2020,1,6), datetime.date(2020,2,6), alpha=0.2, color='red')
    plt.xticks(rotation=45)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax.text(0.065, 0.14, "Baseline Period:       January 2020", transform=ax.transAxes, fontsize=12, rotation=90)
    
    fig.savefig("../img/us_mobility_all.png", dpi=400, bbox_inches='tight')
