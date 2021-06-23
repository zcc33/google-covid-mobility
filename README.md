# COVID Mobility Trends

## Table of Contents

1. [Overview](#overview)
2. [Description of Data](#description)
3. [Data Processing](#processing)
4. [Overall Mobility Trends (US)](#overall)
5. [State-Level Example (MD)](#state)
7. [Comparison of Immobility Across States](#comparison)
8. [Hypothesis Testing for "Granger Causality"](#testing)
9. [Conclusions and Future Work](#future)



## Overview <a name ="overview"> </a>
The COVID-19 outbreak disrupted almost every aspect of people's lives, and particularly their movement patterns. As lockdowns, shutdowns, quarantines, restrictions, and social distancing became ubiquitous, people found themselves spending more time in places like parks and their own residences, and less time at work, transit stations, retail locations, etc. As part of their [COVID-19 Open Data Set](https://github.com/GoogleCloudPlatform/covid-19-open-data), Google released anonymized, aggregated mobility data across different regions obtained from users' cell phones. We took a look at this extensive data to 1) confirm general mobility trends for the US, 2) compare mobility changes against other pandemic variables, 3) compare different states' degree of immobility, and 4) test whether stringency of lockdown measures can predict immobility patterns.

## Description of Data <a name ="description"> </a>

The COVID-19 Open Data Set contains daily time series data of over 500 variables for over 20,000 locations. For location, we focused on the US and individual states. For features, we focused on mobility trends. We additionally looked at variables such as `stringency_index`, which summarizes the degree of enforced distancing imposed by a region's government. The entire dataset is stored on the Google Cloud Platform and can be easily explored [there](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=covid19_open_data) using SQL. Location-specific subsets can be downloaded by using a specific location key, such as `US` for the entire United States, and `US_MD` for the state of Maryland.

 Descriptions of the mobility data can be found [here](https://github.com/GoogleCloudPlatform/covid-19-open-data/blob/main/docs/table-mobility.md) and [here](https://www.google.com/covid19/mobility/).  Descriptions of the stringency index and its associated governmental measures can be found [here](https://github.com/GoogleCloudPlatform/covid-19-open-data/blob/main/docs/table-government-response.md).

| Variable | Description | What it measures |
| --- | --- | --- | 
| mobility_retail_and_recreation | Places like restaurants, cafes, shopping centers, theme parks, museums, libraries, and movie theaters  | Percent (%) change in number of visits |
| mobility_grocery_and_pharmacy | Places like grocery markets, food warehouses, farmers markets, specialty food shops, drug stores, and pharmacies | Percent (%) change in number of visits |
| mobility_parks | Places like local parks, national parks, public beaches, marinas, dog parks, plazas, and public gardens | Percent (%) change in number of visits |
| mobility_transit_stations | Places like public transport hubs such as subway, bus, and train stations | Percent (%) change in number of visits |
| mobility_workplaces | Places of work | Percent (%) change in number of visits | 
| mobility_residential | Places of residence | Percent (%) change in  time spent |
| stringency_index | Overall severity of government controls, such as school/work closings, transport shutdowns, public event cancellations, restrictions on gatherings, etc. | An index from 0 (least severe) to 100 (most severe) |

### Limitations of the Data

1. These are cell phone data gathered from smart phone users who have Google Location Tracking enabled. This may not be representative of those who do not own smart phones, those who have not enabled Google Location Tracking, those who do not use Google services, and those who go to places where cell phones are not needed or not allowed.

2. We do not have access to absolute values, but rather only percentage change compared to a fixed baseline. This baseline was in the month of January 2020, immediately preceding the pandemic. Since this baseline was in the middle of winter, mobility changes thereafter would likely be influenced by the weather as well as by the impacts of the pandemic. For example, it is hard to tell how much the increase in Park visits during June 2020 was due to the lockdowns, versus the warmer weather. So one should be careful about comparing across different times of the year (in addition to other factors like holidays, region-specific events, etc.)

3. Location categorizations and accuracy are somewhat region-specific. One should be careful about directly comparing regions which are far apart and/or very different in culture.

## Data Processing <a name ="processing"> </a>
We processed the data as follows:

1. **Time series smoothing** - We noticed the data exhibited a large amount of choppiness by day of the week, particularly between weekdays and weekends. This makes sense beacuse the mobility data were calculated with reference to a specific day of the week. So we took a 7-day moving average to smooth out the bumpiness.
2. **Interpolate/forward-fill missing values** - There were a lot of single missing values in the mobility variables, which we interpolated from surrounding values. There were also slightly longer chunks of missing values in stringency index, which we we forward-filled from preceding values.
3. **Remove extreme outliers (reporting errors)** - We forward-filled occasional extreme outliers (95%+ drops) in variables like cumulative vaccinated and confirmed cases. These were likely reporting errors, which got corrected by the next reporting day, but which were causing large irregularities when graphed.


## Overall Mobility Trends (US) <a name ="overall"> </a>

To illustrate general trends, we plotted US mobility variables over the entire duration of the outbreak. Note the baseline period shaded in red. 

![](img/us_mobility_all.png)

Observations:

* **Retail/Grocery/Transit/Workplaces**: These categories are highly correlated, dipping sharply at the outset of the pandemic, recovering somewhat and remaining significantly below baseline into the present day. It appears grocery mobility (labeled in orange) spiked for a few days as people went out to stock up on supplies in the very early days. Grocery mobility seems to be least affected by the pandemic, since people still need to buy food and essentials. Retail and recreation seems to have made a decent recovery. Workplaces and transit stations were the hardest hit and remain flat into the present day.
* **Residential**: This was the only variable that measured change in total time spent, rather than number of visits. As one would expect, reduced mobility in the other categories correponds with increase in residential mobility. Since it's a percentage change in total time spent, this variable is inherently capped. There's only 24 hours in a day and people already spent a considerable amount of their time at home before the pandemic.
* **Parks**: This was an idiosyncratic category. Since parks do not contribute as much to virus spread, it's likely that park mobility would increase as a substite for other activities. At the same time, parks are the most influenced by seasonality of weather. Since the baseline was in January, we would naturally expect park attendance to increase dramatically moving into summer. What we see is a slight dip in the beginning along with everything else, and then a sustained rise throughout the warmer months. Park attendance was noticeably down in January 2021, without the effects of seasonality, so perhaps the effect of the pandemic on park attendance is in fact negative.


## State-Level Example (MD) <a name ="state"> </a>

We explored state-level data for Maryland and plot some mobility trends against variables associated with lockdowns and the virus spread.

![](img/md_mobility_specific.png)


**Retail Mobility vs. New Cases** - Retail mobility seems loosely related to the number of new cases. Retail mobility plummeted in the early days of the pandemic, but began recovering even as new cases reached a local maximum around May/April 2020. As new cases peaked in the winter of 2020/2021, retail mobility began declining but never to the levels seen in the early days of the pandemic. More recently, as new cases has fallen precipitously, retail mobility is steadily climbing and has almost reached baseline.

**Residential Mobility vs. Stringency Index** - There is an almost perfect correspondence between residential mobility and stringency index. As stringency rose and gradually declined into the pandemic, the amount of time spent at home seems to have followed in unison. Perhaps lockdown policies are indeed effective and can be seen most clearly in residential mobility.

**Transit Mobility vs. Total Vaccinations** - Widespread vaccinations have not led to full recovery of transit stations. While total vaccinations hit 3 million, transit mobility is lagging at -30% off baseline. It may take a while before people are ready to return to transit stations.


## Comparison of Immobility Across States <a name ="comparison"> </a>
We wanted to compare how different states' movement patterns were affected by the pandemic. More specifically, which states had the most reduced mobility? To this effect, we introduced an `immobility_index` which took the average of retail/grocery/workplace/transit variables across the following 4 weeks:

> 1. The 2 weeks following the date of max stringency (unique for each state). This reflects the immediate and most acute response to the pandemic.
> 2. The 2 weeks in the middle of January 2021. This serves as a direct comparator with the baseline, removing effects of seasonality.

Then we normalized to get an `immobility_score`. The most immobile state gets a maximum score of 100.

![](img/state_comparison_head.png)

The most immobile states are Massachusetts, New York, New Jersey, etc. We see almost entirely Northeastern and Pacific West Coast states. They tend to be larger, urban, and more densely populated. This makes sense. States that have a larger population and density have a greater need to practice social distancing to prevent virus spread.

![](img/state_comparison_tail.png)

The bottom 10 states include Mississippi, Wyoming, Arkansas, etc. We see mostly rural states from the South and Mountain West. Accordingly, their lower population densities allows for reduced social distancing measures. There may also be cultural and political factors at play. The immobility indices of bottom 10 states (-20%) show their movement reductions were roughly half that of the top 10 immobile states (-40%).

To see the full table, click [here](img/state_comparison.png).


## Hypothesis Testing for Granger causuality <a name ="testing"> </a>
Hypothesis testing is difficult for time series because the data points are not independent. However, there is a testable concept called Granger causality which was developed specifically for time series. 

From [Wikipedia](https://en.wikipedia.org/wiki/Granger_causality):

> A time series X is said to Granger-cause Y if it can be shown, usually through a series of t-tests and F-tests on lagged values of X (and with lagged values of Y also included), that those X values provide statistically significant information about future values of Y. 

Note that, despite the name, Granger causality is far from implying true causality.

We hypothesized that, across the United States, the stringency index would Granger-cause retail mobility. In other words, changes in public policy (either tightening or loosening of restrictions) would contain predictive information about people's movement patterns, particularly to discretionary locations like retail.

To conduct the test, we used the `grangercausalitytests` function from the `statsmodels.tsa.stattools` module. We picked the period from February 25, 2020 to June 1, 2021, which contains a large number of time points over different stages of the pandemic. For the testing, we chose a max lag value of 7 corresponding to the number of days in the week, although there are more rigorous ways of doing this. 

An important assumption for Granger causality testing is that the series be stationary. We took the series' first-order differences to remove non-stationarity, and ran the test on the differenced series. The p=values corresponding to the ssr-based F test for Granger causality are reported below, for each lag value.


> Null hypothesis: `stringency_index` does not Granger-cause `mobility_retail_and_recreation`. 

> We select our alpha level to be 0.05. We reject the null hypothesis if the p-value is below 0.05.

| Lag value | p-value (differenced series) |
| --- | ---|
| 1 | 0.0000 |
| 2 | 0.0000 |
| 3 | 0.0000 |
| 4 | 0.0000 |
| 5 | 0.0001|
| 6 | 0.0002|
| 7 | 0.0000|

All the p-values are low enough to reject the null hypothesis individually. And even with a Bonferroni correction to account for the multiple comparisons, we can safely reject our null hypothesis at the alpha=0.05 confidence level. Therefore, we conclude that `stringency_index` does Granger-cause `mobility_retail_and_recreation`.


## Conclusions and Future Work <a name ="future"> </a>

In this project we explored the Google mobility data (part of the COVID-19 Open Data Set), the first of its kind to be released for public use. Despite having limitations, the dataset provides insights into mobility trends during the COVID pandemic at various geographical scales. 

Overall, we found that non-residential mobility dropped steeply in the early days of the pandemic, recovering somewhat in the summer of 2020, and plateauing at a rate significantly below baseline into the present day. The most reduced have been workplace and transit mobility. Grocery store mobility was least affected throughout the pandemic. Retail mobility was heavily affected in the beginning but has shown an impressive recovery. Park mobility increased dramatically during the summer, but this may have been due to the seasonality of warmer weather.

We created an immobility score to compare reductions in mobility among states. We determined that the most immobile states (e.g. Massachusetts, New York, New Jersey) were predominantly large, urban, densely populated, and located in the North East or Pacific West Coast. Meanwhile the least immobile states (e.g., Wyoming, Mississippi, Arkansas) were rural and less densely populated. They were all located in the South or Mountain West.

Hypothesis testing for Granger causality showed that stringency index contains predictive information about retail mobility, which accords with our intutions about the lockdown measures having an effect on people's discretionary movement patterns.

In future work, we would like to apply additional time series methods to the data. More attention should be paid to the assumptions of the Granger causality testing, and how the lag values are chosen. Annother interesting direction would be investigating the length of delay, or lag, between various virus indicators and mobility reduction, or between stringency index and mobility reduction, both within states and across states.
## References

1. https://console.cloud.google.com/marketplace/product/bigquery-public-datasets/covid19-open-data
2. https://github.com/GoogleCloudPlatform/covid-19-open-data
3. https://www.google.com/covid19/mobility/
4. https://en.wikipedia.org/wiki/Granger_causality
5. https://stackoverflow.com/questions/19726663/how-to-save-the-pandas-dataframe-series-data-as-a-figure