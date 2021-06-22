import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from clean_data import clean_data

"""
  Calculate state's immobility index - a single number representing how much social
  mobility declined during the COVID pandemic.

  The following mobility variables were used:
    retail_and_recreation, grocery_and_pharmacy, transit_stations, workplaces

  Residential and parks were excluded given their inverse relationship with the pandemic.

  Index calculated as the 4 variables' average across:
    1. the 2 weeks immediately following the state's maximum stringency index
    2. the 2 weeks in the middle of January 2021, as direct contrast with baseline

  Parameters:
  -----------
  df (DataFrame): cleaned dataset for a particular state

  Returns
  -------
  index (float): immobility index for state
  """

def immobility_index(df):
    immobility_var = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_transit_stations", "mobility_workplaces"]
    max_strin = df.idxmax()["stringency_index"]

    #2 weeks immediately following max stringency
    days_range1 = list(pd.date_range(start=max_strin, end=max_strin + datetime.timedelta(days=14)))
    #2 weeks in the middle of January 2021
    days_range2 = list(pd.date_range(start = "2021-01-10", end = "2021-01-24"))

    df_restricted = df.loc[days_range1+days_range2,:]
    index = df_restricted.mean()[immobility_var].sum()/4

    return index

"""
  Creates immobility score by normalizing immobility indices. Higher the score, the more immobile the state.

  Most immobile state will have a score of 100.
  Not a strict normalization - least mobile state has a score > 0.

  Parameters:
  -----------
  df (DataFrame): state immobility index DataFrame

  Returns
  -------
  none, changes to df are made in-place
  """
def immobility_scores(df):
    df["immobility_score"] = round((df["immobility_index"]/df["immobility_index"].min())*100, 1)

"""
  Render the contents of a DataFrame as an image in table format. It turns out there's no
  built-in way to do this. Credit for this function goes to the following StackExchange thread:
  https://stackoverflow.com/questions/19726663/how-to-save-the-pandas-dataframe-series-data-as-a-figure

  Parameters:
  -----------
  data (DataFrame): DataFrame to turn into an image
  col_width (float): width of a single table column
  row_height( float): height of a single table row
  font_size (float): size of font

  Returns
  -------
  fig, ax: figure and axis for rendered table image
  """
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

"""
Compare the 50 US states by how immobile they became as a result of the COVID pandemic.
First calculate an immobility index for each state based on mobility variables. Then an immobility score.
See function descriptions above for details.

Sort the states by immobility score (most immobile first) and saves the dataframe as image in table format.

Save entire table, top 10 states, and bottom 10 states as:
../img/state_comparison.png
../img/state_comparison_head.png
../img/state_comparison_tail.png
"""
if __name__ == "__main__":
    mobility = ["mobility_retail_and_recreation", "mobility_grocery_and_pharmacy", "mobility_parks", "mobility_transit_stations", "mobility_workplaces", "mobility_residential"]
    restrictions = ["school_closing", "workplace_closing", "cancel_public_events","restrictions_on_gatherings", "public_transport_closing", "stay_at_home_requirements", "restrictions_on_internal_movement", "stringency_index"]
    virus = ["new_confirmed", "cumulative_persons_fully_vaccinated"]

    #get the location keys for US states
    index_df = pd.read_csv("../data/index.csv")
    states_index = index_df.loc[(index_df.country_code == "US") & (index_df.aggregation_level==1), :]
    state_keys = list(states_index["key"])
    state_names=list(states_index["subregion1_name"])
    #create data frame with state names and location keys, excluding non-state territories
    data = {"key": state_keys, "name": state_names, "immobility_index":np.zeros(len(state_keys)), "avg_stringency":np.zeros(len(state_keys))}
    state_df = pd.DataFrame(data).set_index("key")
    state_df = state_df.drop(["US_AS", "US_GU", "US_MP", "US_PR", "US_VI", "US_DC"])
    
    #calculate the immobility index for each state
    for key in state_df.index:
        print("Working on " + key)
        df = pd.read_csv(f'https://storage.googleapis.com/covid19-open-data/v3/location/{key}.csv', parse_dates=["date"], index_col="date")
        df = clean_data(df)
        state_df.loc[key, "immobility_index"] = round(immobility_index(df),1)
        state_df.loc[key, "avg_stringency"] = round((df["stringency_index"].max()+df["stringency_index"].loc["2021-01-15"])/2, 1)

    #normalize the immobility indices into immobility scores
    immobility_scores(state_df)

    #sort by immobility score, descending
    state_df = state_df.sort_values(by=["immobility_score"], ascending=False)
    state_df=state_df[["name", "immobility_score", "immobility_index", "avg_stringency"]]

    #save entire dataframe as table image
    fig,ax = render_mpl_table(state_df, header_columns=0, col_width=3.5)
    fig.savefig("../img/state_comparison.png", dpi=400, bbox_inches='tight')

    #save the top 10 immobile states as table image
    fig,ax = render_mpl_table(state_df.head(10), header_columns=0, col_width=3.5)
    ax.set_title("Top 10 States by Immobility Score", fontsize=18, fontweight='bold')
    fig.savefig("../img/state_comparison_head.png", dpi=400, bbox_inches='tight')

    #save the bottom 10 immobile states as table image
    fig,ax = render_mpl_table(state_df.tail(10), header_columns=0, col_width=3.5)
    ax.set_title("Bottom 10 States by Immobility Score", fontsize=18, fontweight='bold')
    fig.savefig("../img/state_comparison_tail.png", dpi=400, bbox_inches='tight')