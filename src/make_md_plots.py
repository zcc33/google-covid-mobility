import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from clean_data import clean_data

"""
Makes MD-specific plots showing:
    1. Retail mobility vs. new COVID cases
    2. Residential mobility vs. stringency index
    3. Transity mobility vs. cumulative vaccinations

Saves all 3 plots as single image in ../img/md_mobility_specific.png
"""

if __name__ == "__main__":
    #download and clean US_MD dataset
    data_key = "US_MD"
    df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{data_key}.csv', parse_dates=["date"], index_col="date")
    df = clean_data(df)

    #take the time window as Jan. 1 2020 to June 8 2021
    date_window = pd.date_range(start = "2020-01-01", end = "2021-06-8")
    df_plot=df.loc[date_window,:]

    fig, axs = plt.subplots(3, sharex=True, figsize=(10,12),dpi=400)
    fig.suptitle('State-Level Trends for Maryland (US_MD)', size = 16)

    #plot retail mobility vs. new COVID cases
    axs[0].plot(df_plot.index, df_plot[["mobility_retail_and_recreation"]])
    axs[0].set_xlabel("")
    axs[0].set_ylabel("Retail Change (%)", fontsize=15, color="#1f77b4")
    axs[0].set_title("Retail Mobility vs. New Cases", fontsize = 15)
    ax2 = axs[0].twinx()
    ax2.plot(df_plot.index, df_plot["new_confirmed"], color="red")
    ax2.set_ylabel("New Cases", color = "red", fontsize = 15)

    #plot residential mobility vs. stringency index
    axs[1].plot(df_plot.index, df_plot[["mobility_residential"]], color="#1f77b4")
    axs[1].set_xlabel("")
    axs[1].set_ylabel("Residential Change (%)", fontsize=15, color="#1f77b4")
    axs[1].set_title("Residential Mobility vs. Stringency Index", fontsize = 15)
    axs[1].set_ylim(-5,30)
    ax2 = axs[1].twinx()
    ax2.plot(df_plot.index, df_plot["stringency_index"], color="red")
    ax2.set_ylabel("Stringency Index (Max 100)", color = "red", fontsize = 15)

    #plot transit mobility vs. total vaccinations
    axs[2].plot(df_plot.index, df_plot[["mobility_transit_stations"]], color="#1f77b4")
    axs[2].set_xlabel("")
    axs[2].set_ylabel("Transit Change (%)", fontsize=15, color="#1f77b4")
    axs[2].set_title("Transit Mobility vs. Total Vaccinations", fontsize = 15)
    ax2 = axs[2].twinx()
    ax2.plot(df_plot.index, df_plot["cumulative_persons_fully_vaccinated"], color="red")
    ax2.set_ylabel("Total Vaccinated", color = "red", fontsize = 15)

    fig.savefig("../img/md_mobility_specific.png", dpi=400, bbox_inches='tight')
