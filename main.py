from json import load
from src.etlGYGdata import etlGYGdata
from src.etlIntTourismData import etlIntTourismData

# Gsheet service account. You need your own to upload data into Gsheet
gsheet_dict = load(open(file="gsuite_service_account.json"))

# URL to the gsheet
ss = "https://docs.google.com/spreadsheets/d/1uvEvq4I43SvUU5_2TfyjVr4PbSzPj6nU6iyVjUrJL_M/edit#gid=0"

# Extracts, transforms and load the international tourism data
etlIntTourismData(ss=ss, gsheet_dict=gsheet_dict)

# Extracts, transforms and load GetYourGuide data from webserver
etlGYGdata(gsheet_dict=gsheet_dict, ss=ss)
