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

    data_key = "US"
    df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{data_key}.csv', parse_dates=["date"], index_col="date")
    df=df[mobility+restrictions+virus]
    clean_data(df)

    date_window = pd.date_range(start = "2020-01-01", end = "2021-06-8")
    df_plot=df.loc[date_window,:]
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
