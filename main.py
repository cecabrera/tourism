from pandas import read_csv, melt, concat, pivot_table, NA
from json import load
from src.write_sheet import write_sheet

gsheet_dict = load(open(file="gsuite_service_account.json"))
ss = "https://docs.google.com/spreadsheets/d/1uvEvq4I43SvUU5_2TfyjVr4PbSzPj6nU6iyVjUrJL_M/edit#gid=0"

main_colnames = [
    'Country Name',
    'Country Code',
    'Indicator Name',
    'Indicator Code']

df1 = read_csv(filepath_or_buffer="data/API_ST.INT.ARVL_DS2_en_csv_v2_1927083.csv")
df2 = read_csv(filepath_or_buffer="data/API_ST.INT.DPRT_DS2_en_csv_v2_1929304.csv")
df3 = read_csv(filepath_or_buffer="data/API_ST.INT.XPND.CD_DS2_en_csv_v2_1929314.csv")

year_colnames = [x for x in df1.columns if x not in main_colnames]
df1 = melt(
    frame=df1,
    value_vars=year_colnames,
    id_vars=main_colnames,
    var_name="Year",
    ignore_index=True,
    value_name="Value")

df2 = melt(
    frame=df2,
    value_vars=year_colnames,
    id_vars=main_colnames,
    var_name="Year",
    ignore_index=True,
    value_name="Value")

df3 = melt(
    frame=df3,
    value_vars=year_colnames,
    id_vars=main_colnames,
    var_name="Year",
    ignore_index=True,
    value_name="Value")

df = concat(objs=[df1, df2], ignore_index=True, verify_integrity=True)
df = concat(objs=[df, df3], ignore_index=True, verify_integrity=True)

df = df.loc[~df['Value'].isna()]

df = pivot_table(
    data=df,
    columns="Indicator Name",
    aggfunc=sum,
    index=["Country Name", "Year"]).reset_index()

df.columns = df.columns.droplevel()

cols = df.columns.to_list()
cols[0], cols[1] = ["Country Name", "Year"]
df.columns = cols

# Extract regions
regions = df.loc[
    (df['International tourism, expenditures (current US$)'] > 30000000000) | \
        (df['Country Name'].isin([
            "Small states",
            "Other small states"
        ]))
    , 'Country Name'].unique()

# Omit huge countries
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

regions = [x for x in regions if x not in omit_regions]

df['Region'] = df['Country Name']
df.loc[~df['Country Name'].isin(regions), "Region"] = "Country"

df['Investment per arrival'] = df['International tourism, expenditures (current US$)'] / df['International tourism, number of arrivals']
df['Investment per departure'] = df['International tourism, expenditures (current US$)'] / df['International tourism, number of departures']
df['Arrival per departure'] = df['International tourism, number of arrivals'] / df['International tourism, number of departures']

write_sheet(
    df=df,
    service_account_dict=gsheet_dict,
    sheet="Tourism",
    overwrite=True,
    ss=ss)