# COVID Mobility Trends

## Table of Contents

1. [Overview](#overview)
2. [Description of Data](#description)
3. [Data Processing](#processing)
4. [Overall Mobility Trends (US)](#overall)
5. [State-Level Example (MD)](#state)
7. [Comparison of Immobility Across States](#comparison)
8. [Hypothesis Testing for "Granger Causality"](#testing)
9. [Future Work](#future)



## Overview <a name ="overview"> </a>
The COVID-19 outbreak disrupted almost every aspect of people's lives, and nowhere could this be seen more clearly than in our movement patterns. As lockdowns, shutdowns, quarantines, restrictions, and social distancing became the norm--and the law--people found themselves spending much more time in places like parks and their own residences, and much less time at work, transit stations, or retail locations. As part of their [COVID-19 Open Data Set](https://github.com/GoogleCloudPlatform/covid-19-open-data), Google released anonymized, aggregated mobility data across different regions obtained from users' cell phones. Within this data, we can see the sheer magnitude of movement changes that have been brought about by COVID, and begin to identify some key trends and patterns.

## Description of Data <a name ="description"> </a>

The COVID-19 Open Data Set contains daily time series data of over 500 variables for over 20,000 locations. We mainly focused on the subset of US states and the variables related to mobility trends. We additionally looked at some other variables such as `stringency_index`, which summarizes the degree of enforced distancing imposed by a region's government. The entire dataset is stored on the Google Cloud Platform and can be freely queried [there](https://console.cloud.google.com/bigquery?p=bigquery-public-data&d=covid19_open_data) using SQL. Location-specific subsets be downloaded by using a specific location key, such as `US` for the entire United States, and `US_MD` for the state of Maryland.

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

There are three important limitations of the mobility data.

The first is that these are cell phone data gathered from smart phone users who have Google Location Tracking enabled. This may not be representative of those who do not own smart phones, those who have not enabled Google Location Tracking, those who do not use Google services, and those who go to places where cell phones are not needed or not allowed.

Secondly, we do not have access to absolute values, but rather only percentage change compared to a fixed baseline. This baseline was in the month of January 2020, immediately preceding the pandemic. Since this baseline was in the middle of winter, mobility changes thereafter would likely be influenced by the weather as well as the impacts of the pandemic. For example, it is hard to tell how much the increase in Park visits during June 2020 was due to the lockdowns, versus the warmer weather. So one should be careful about comparing across different times of the year (in addition to other factors like holidays, region-specific events, etc.)

Thirdly, categorizations and accuracy are somewhat location-specific. One should be careful about directly comparing regions which are far apart and/or very different in culture.

## Data Processing <a name ="processing"> </a>
The processing of the data could be roken dow

1. Time series Smoothing - The mobility data 
2. Missing Values Interpolation - 
3. 


## Overall Mobility Trends (US) <a name ="overall"> </a>

When graphing the overall mobility trends for the US, we see that 
![](img/us_mobility_all.png)


## State-Level Example (MD) <a name ="state"> </a>

![](img/md_mobility_specific.png)

## Comparison of Immobility Across States <a name ="comparison"> </a>



## Hypothesis Testing for Granger causuality <a name ="testing"> </a>
In general it's difficult to conduct hypothesis tests on time series because the data points are not independent of each other. However, there is a testable notion called "Granger causality" which was developed specifically for time series. 

> Definition: Time series A is said to Granger-cause timee series B if A contains predictive information about B beyond what is contained in the previous values of B.

Note that, despite the name, Granger causality is far from implying true causality.

We hypothesized that, across the United States, the stringency index (how it changes over time) would Granger-cause the mobility trends to retail locations we observe. In other words, changes in public policy (either tightening or loosening of restrictions) would contain predictive information about people's movement patterns, particularly to discretionary locations like retail.

To conduct the test, we used the `grangercausalitytests` function from the `statsmodels.tsa.stattools` module. We ran the tests on stringency index and retail mobility for the United States over the period from February 25, 2020 to June 1, 2021. This contains a large selection of time points over different stages of the pandemic. For the testing, we chose a max lag value of 7 corresponding to the number of days in the week, although there are more rigorous ways of doing this. We conducted the tests both for the raw series and for versions of the series which were differenced to partially remove non-stationarity. The p=values corresponding to the ssr-based F test for Granger causality are reported below, for each lag value.


> Null hypothesis: `stringency_index` does **not** Granger-cause `mobility_retail_and_recreation`. 

> We select our alpha level to be 0.05, so we reject the null hypothesis if the p-value is below 0.05.

| Lag value | p-value (raw series)| p-value (differenced series) |
| --- | --- | ---|
| 1 | 0.0310| 0.0000 |
| 2 | 0.0003| 0.0000 |
| 3 | 0.0000| 0.0000 |
| 4 | 0.0001| 0.0000 |
| 5 | 0.0002| 0.0001|
| 6 | 0.0008| 0.0002|
| 7 | 0.0010| 0.0000|

We see that all the p-values are low enough to reject the null hypothesis individually. However, for the raw series with a time lag of 1, the p-value is 0.03, which although less than 0.05, would not allow us to reject after performing a Boneferroni correction for conducting multiplie comparisons. Therefore, we cannot reject the null hypothesis; however tempting, we cannot claim that stringency index Granger-causes retail mobility.


## Future Work <a name ="future"> </a>
1. It would be interesting
2.  


&nbsp;
&nbsp;

<br></br>


* Unordered
    * List

*  This is the first list item.
*  Here's the second list item.

    > A blockquote would look great below the second list item.

*   And here's the third list item.

**bold**

## References

1. https://console.cloud.google.com/marketplace/product/bigquery-public-datasets/covid19-open-data
2. https://github.com/GoogleCloudPlatform/covid-19-open-data
3. https://www.google.com/covid19/mobility/
4. https://en.wikipedia.org/wiki/Granger_causality
5. https://stackoverflow.com/questions/19726663/how-to-save-the-pandas-dataframe-series-data-as-a-figure