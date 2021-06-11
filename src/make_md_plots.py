import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

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

    data_key = "US_MD"
    df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{data_key}.csv', parse_dates=["date"], index_col="date")
    df=df[mobility+restrictions+virus]
    clean_data(df)

    date_window = pd.date_range(start = "2020-01-01", end = "2021-06-8")
    df_plot=df.loc[date_window,:]
    fig, axs = plt.subplots(3, sharex=True, figsize=(10,12),dpi=400)

    date_window = pd.date_range(start = "2020-01-01", end = "2021-06-8")
    df_plot=df.loc[date_window,:]
    fig, axs = plt.subplots(3, sharex=True, figsize=(10,12),dpi=400)
    fig.suptitle('State-Level Trends for Maryland (US_MD)', size = 16)

    axs[0].plot(df_plot.index, df_plot[["mobility_retail_and_recreation"]])
    axs[0].set_xlabel("")
    axs[0].set_ylabel("Retail Change (%)", fontsize=15, color="#1f77b4")
    axs[0].set_title("Retail Mobility vs. New Cases", fontsize = 15)
    ax2 = axs[0].twinx()
    ax2.plot(df_plot.index, df_plot["new_confirmed"], color="red")
    ax2.set_ylabel("New Cases", color = "red", fontsize = 15)

    axs[1].plot(df_plot.index, df_plot[["mobility_residential"]], color="#1f77b4")
    axs[1].set_xlabel("")
    axs[1].set_ylabel("Residential Change (%)", fontsize=15, color="#1f77b4")
    axs[1].set_title("Residential Mobility vs. Stringency Index", fontsize = 15)
    axs[1].set_ylim(-5,30)
    ax2 = axs[1].twinx()
    ax2.plot(df_plot.index, df_plot["stringency_index"], color="red")
    ax2.set_ylabel("Stringency Index (Max 100)", color = "red", fontsize = 15)

    axs[2].plot(df_plot.index, df_plot[["mobility_transit_stations"]], color="#1f77b4")
    axs[2].set_xlabel("")
    axs[2].set_ylabel("Transit Change (%)", fontsize=15, color="#1f77b4")
    axs[2].set_title("Transit Mobility vs. Total Vaccinations", fontsize = 15)
    ax2 = axs[2].twinx()
    ax2.plot(df_plot.index, df_plot["cumulative_persons_fully_vaccinated"], color="red")
    ax2.set_ylabel("Total Vaccinated", color = "red", fontsize = 15)

    fig.savefig("../img/md_mobility_specific.png", dpi=400, bbox_inches='tight')
