import pandas as pd

"""
  Cleans DataFrame by:
    1. subsetting the mobility, restrictions, and virus variables
    2. interpolating / forward-filling missing values
    3. removing extreme outliers (errors) from new_confirmed and cumulative_persons_fully_vaccinated
    4. smooths mobility and virus variables by taking the 7-day moving average

  Parameters:
  -----------
  df (DataFrame): full data from Google COVID-19 Open Dataset by particular location key

  Returns
  -------
  df (DataFrame): Cleaned data, not in-place
  """

def clean_data(df):
    #subset mobility, restrictions, and virus variables
    mobility = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks", "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]
    restrictions = ["school_closing", "workplace_closing", "cancel_public_events","restrictions_on_gatherings", "public_transport_closing", "stay_at_home_requirements", "restrictions_on_internal_movement", "stringency_index"]
    virus = ["new_confirmed", "cumulative_persons_fully_vaccinated"]
    df=df[mobility+restrictions+virus].copy()

    #interpolate missing mobility & virus variables (max 2 days); forward fill missing restriction variables (max 7 days)
    df[mobility] = df[mobility].interpolate(limit=2)
    df[restrictions] = df[restrictions].fillna(method="ffill", limit=7)
    df[virus] = df[virus].interpolate(limit=2)

    #removes outliers by forward-fill when a value suddenly drops by 95% from previous value
    for i in range(1,df.shape[0]):
        previous = df.at[df.index[i-1], "new_confirmed"]
        current = df.at[df.index[i], "new_confirmed"]
        if not pd.isnull(previous) and not pd.isnull(current) and current < 0.05*previous:
            df.loc[df.index[i], "new_confirmed"] = previous
    
    #removes outliers by forward-fill when a value suddenly drops by 95% from previous value
    for i in range(1,df.shape[0]):
        previous = df.at[df.index[i-1], "cumulative_persons_fully_vaccinated"]
        current = df.at[df.index[i], "cumulative_persons_fully_vaccinated"]
        if not pd.isnull(previous) and not pd.isnull(current) and current < 0.05*previous:
            df.loc[df.index[i],"cumulative_persons_fully_vaccinated"] = previous

    #smooths mobility and virus variables by taking the 7-day moving average
    df[mobility] = df[mobility].rolling(7, center=True).mean()
    df[virus] = df[virus].rolling(7, center=True).mean()

    return df