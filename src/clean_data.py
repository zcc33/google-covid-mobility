
def clean_data(df):
    df[mobility] = df[mobility].interpolate(limit=2)
    df[restrictions] = df[restrictions].fillna(method="ffill", limit=5)
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