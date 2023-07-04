from pandas import pivot_table, DataFrame


def setDf(df: DataFrame) -> DataFrame:

    """
    Function to transform the data into a readable format for dashboard
    visualization
    """

    # Omit null values
    df = df.loc[~df['Value'].isna()]

    # Transform data to set indicators as columns
    df = pivot_table(
        data=df,
        columns="Indicator Name",
        aggfunc=sum,
        index=["Country Name", "Year"]).reset_index()

    # Drop first level on pivot table
    df.columns = df.columns.droplevel()

    # Set column names
    cols = df.columns.to_list()
    cols[0], cols[1] = ["Country Name", "Year"]
    df.columns = cols

    # Extract regions
    regions = df.loc[
        (df['International tourism, expenditures (current US$)'] > 30000000000) | \
            (df['Country Name'].isin([
                "Small states",
                "Other small states",
                "IDA only"
            ]))
        , 'Country Name'].unique()

    # Omit big countries
    omit_regions = [
        "China",
        "United States",
        "Germany",
        "France",
        "Spain",
        "United Kingdom",
        "Russian Federation",
        "Georgia",
        "Australia",
        "Canada",
        "Korea, Rep.",
        "Japan",
        "Spain",
        "Italy"]

    # Filter regions
    regions = [x for x in regions if x not in omit_regions]

    # Set regions
    df['Region'] = df['Country Name']
    df.loc[~df['Country Name'].isin(regions), "Region"] = "Country"

    # Set insights
    df['Investment per arrival'] = df['International tourism, expenditures (current US$)'] / df['International tourism, number of arrivals']
    df['Investment per departure'] = df['International tourism, expenditures (current US$)'] / df['International tourism, number of departures']
    df['Arrival per departure'] = df['International tourism, number of arrivals'] / df['International tourism, number of departures']

    # rename column names
    df.rename(columns={
        'International tourism, expenditures (current US$)': "Invesment in tourism",
        'International tourism, number of arrivals': "Number of arrivals",
        'International tourism, number of departures': "Number of departures",
        }, inplace=True)

    # Sort values
    df.sort_values(by=["Year", "Country Name"], ascending=[False, True], inplace=True)

    return df