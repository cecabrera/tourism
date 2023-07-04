from pandas import read_csv, melt, concat, DataFrame

main_colnames = [
    'Country Name',
    'Country Code',
    'Indicator Name',
    'Indicator Code']


def readMergeCSV() -> DataFrame:

    """
    Function to read and merge the CSV files into one single dataframe
    """

    # Read each file
    df1 = read_csv(filepath_or_buffer="data/API_ST.INT.ARVL_DS2_en_csv_v2_1927083.csv")
    df2 = read_csv(filepath_or_buffer="data/API_ST.INT.DPRT_DS2_en_csv_v2_1929304.csv")
    df3 = read_csv(filepath_or_buffer="data/API_ST.INT.XPND.CD_DS2_en_csv_v2_1929314.csv")

    # Get year's column names
    year_colnames = [x for x in df1.columns if x not in main_colnames]

    # Melt the csv data 1
    df1 = melt(
        frame=df1,
        value_vars=year_colnames,
        id_vars=main_colnames,
        var_name="Year",
        ignore_index=True,
        value_name="Value")

    # Melt the csv data 2
    df2 = melt(
        frame=df2,
        value_vars=year_colnames,
        id_vars=main_colnames,
        var_name="Year",
        ignore_index=True,
        value_name="Value")

    # Melt the csv data 3
    df3 = melt(
        frame=df3,
        value_vars=year_colnames,
        id_vars=main_colnames,
        var_name="Year",
        ignore_index=True,
        value_name="Value")

    # Concat DataFrame 1 with 2
    df = concat(objs=[df1, df2], ignore_index=True, verify_integrity=True)

    # Concat main Dataframe with 3
    df = concat(objs=[df, df3], ignore_index=True, verify_integrity=True)

    return df