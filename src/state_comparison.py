import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

def immobility_index(df):
    immobility = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_transit_stations", "mobility_workplaces"]
    max_strin = df.idxmax()["stringency_index"]
    days_range1 = list(pd.date_range(start=max_strin, end=max_strin + datetime.timedelta(days=14)))
    days_range2 = list(pd.date_range(start = "2021-01-10", end = "2021-01-24"))
    df_restricted = df.loc[days_range1+days_range2,:]
    
    index = df_restricted.mean()[immobility].sum()/4
    return index

def normalize_scores(df):
    df["immobility_score"] = round((df["immobility_index"]/df["immobility_index"].min())*100, 1)


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


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size, dpi=400)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, cellLoc = "left", **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax.get_figure(), ax


if __name__ == "__main__":
    mobility = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks", "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]
    restrictions = ["school_closing", "workplace_closing", "cancel_public_events","restrictions_on_gatherings", "public_transport_closing", "stay_at_home_requirements", "restrictions_on_internal_movement", "stringency_index"]
    virus = ["new_confirmed", "cumulative_persons_fully_vaccinated"]

    index_df = pd.read_csv("../data/index.csv")
    states_index = index_df.loc[(index_df.country_code == "US") & (index_df.aggregation_level==1), :]
    state_keys = list(states_index["key"])
    state_names=list(states_index["subregion1_name"])

    data = {"key": state_keys, "name": state_names, "immobility_index":np.zeros(len(state_keys)), "avg_stringency":np.zeros(len(state_keys))}
    state_df = pd.DataFrame(data).set_index("key")
    state_df = state_df.drop(["US_AS", "US_GU", "US_MP", "US_PR", "US_VI", "US_DC"])
    
    for key in state_df.index:
        print(key)
        df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{key}.csv', parse_dates=["date"], index_col="date")
        df=df[mobility+restrictions+virus]

        clean_data(df)

        state_df.loc[key, "immobility_index"] = round(immobility_index(df),1)
        state_df.loc[key, "avg_stringency"] = round((df["stringency_index"].max()+df["stringency_index"].loc["2021-01-15"])/2, 1)

    normalize_scores(state_df)

    state_df = state_df.sort_values(by=["immobility_score"], ascending=False)
    state_df=state_df[["name", "immobility_score", "immobility_index", "avg_stringency"]]

    fig,ax = render_mpl_table(state_df, header_columns=0, col_width=3.5)
    fig.savefig("../img/state_comparison.png", dpi=400, bbox_inches='tight')

    fig,ax = render_mpl_table(state_df.head(10), header_columns=0, col_width=3.5)
    ax.set_title("Top 10 States by Immobility Score", fontsize=18, fontweight='bold')
    fig.savefig("../img/state_comparison_head.png", dpi=400, bbox_inches='tight')

    fig,ax = render_mpl_table(state_df.tail(10), header_columns=0, col_width=3.5)
    ax.set_title("Bottom 10 States by Immobility Score", fontsize=18, fontweight='bold')
    fig.savefig("../img/state_comparison_tail.png", dpi=400, bbox_inches='tight')
    