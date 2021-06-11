# Covid Mobility Trends

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
The COVID-19 outbreak disrupted almost every facet of people's lives, an in particular their daily movement patterns. As part of COVID-19 Open Data Set, Google has released 

## Description of Data <a name ="description"> </a>

| Variable | Description |
| --- | --- |
| mobility_retail_and_recreation | Two Test |
| mobility_grocery_and_pharmacy | 12132 |    
| mobility_parks | |
| mobility_transit_stations | |
| mobility_workplaces | |
| mobility_residential | | 

## Data Processing <a name ="processing"> </a>



## Overall Mobility Trends (US) <a name ="overall"> </a>
![](img/us_mobility_all.png)


## State-Level Example (MD) <a name ="state"> </a>

![](img/md_mobility_specific.png)

## Comparison of Immobility Across States <a name ="comparison"> </a>

## Hypothesis Testing for Granger causuality <a name ="testing"> </a>
In general it's difficult to conduct hypothesis tests on time series because the data points are not independent of each other. However, there is a testable notion called "Granger causality" which was developed specifically for time series. 

>Definition: Time series A is said to Granger-cause timee series B if A contains predictive information about B beyond what is contained in the previous values of B.

Note that, despite the name, Granger causality is far from implying true causality.

We hypothesized that, across the United States, the stringency index (how it changes over time) would Granger-cause the mobility trends to retail locations we observe. In other words, changes in public policy (either tightening or loosening of restrictions) would contain predictive information about people's movement patterns, particularly to discretionary locations like retail.

To do conduct the test, we used the `grangercausalitytests` function from the `statsmodels.tsa.stattools` module. We ran the tests on stringency index and retail mobility for the . Since the 


>Null hypothesis: `stringency_index` does **not** Granger-cause `mobility_retail_and_recreation`. 

| Lag value | p-value (raw series)| p-value (differenced series) |
| --- | --- | ---|
| 1 | 0.0310| 0.0000 |
| 2 | 0.0003| 0.0000 |
| 3 | 0.0000| 0.0000 |
| 4 | 0.0001| 0.0000 |
| 5 | 0.0002| 0.0001|
| 6 | 0.0008| 0.0002|
| 7 | 0.0010| 0.0000|

Our conclusion is that 


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

https://www.markdownguide.org/basic-syntax/

At the command prompt, type `nano`.

$$f(x) = x^2$$

***


    <html>
      <head>
      </head>
    </html>

My favorite search engine is [Duck Duck Go](https://duckduckgo.com).

<https://www.markdownguide.org>
<fake@example.com>


https://stackoverflow.com/questions/35498525/latex-rendering-in-readme-md-on-github

![equation](https://latex.codecogs.com/gif.latex?f%28x%29%20%3D%20%5Cfrac%7B1%7D%7B2%7D) 


This is [an example][1]

[1]: http://www.google.com
