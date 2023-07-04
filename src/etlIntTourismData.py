from src.readMergeCSV import readMergeCSV
from src.setDf import setDf
from src.write_sheet import write_sheet


def etlIntTourismData(
    ss: str,
    gsheet_dict: dict,
    sheet: str = "Tourism"
) -> None:
    
    """
    Extracts, transforms and loads the Internation Tourism data into Gsheet
    """

    # Read and merge CSV
    df= readMergeCSV()

    # Sets the data frame into dashboard format
    df = setDf(df=df)

    # Export data into GSheet to easily manipulate data
    write_sheet(
        df=df,
        service_account_dict=gsheet_dict,
        sheet=sheet,
        overwrite=True,
        ss=ss)

