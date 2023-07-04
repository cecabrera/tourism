from pandas import DataFrame
from gspread import service_account_from_dict
from gspread_dataframe import set_with_dataframe, get_as_dataframe


def write_sheet(
    df: DataFrame,
    ss: str,
    sheet: str or int,
    service_account_dict: dict = None,
    row: int = 1,
    column: int = 1,
    header: bool = True,
    overwrite: bool = True,
    resize: bool = True,
) -> None:

    """
    Function to upload the infomration from a Data Frame into
    Google Sheets. 
    1. Validate the service account location file
    2. Validate that the service account email has access to the 
        GSheet
    3. Verify the sheet index or name

    Parameters
      ----------
      df : DataFrame
          The data frame
      ss : str
          The Google Sheet html url
      sheet : int or string
          The name of the sheet or number of the sheet

    Returns
      -------
      None

    """

    # Load the client from Json file
    client = service_account_from_dict(service_account_dict)

    # Get Sheets available from sheet variable

    try:
        worksheet = client.open_by_url(url=ss)
        error = False
    except Exception as e:
        pass
        if e.response.json()['error']['status'] == "PERMISSION_DENIED":
            print("User `%s` has not edit permission to Gsheet `%s`" % (
                service_account_dict['client_email'], ss))
        error = True

    if not error:
        sheetnames = [x.title for x in worksheet.worksheets()]

        sheet = sheetnames[sheet] if isinstance(sheet, int) else sheet

        if sheet not in sheetnames:
            print("Worksheet %s does not exist and will be created" % sheet)
            worksheet.add_worksheet(title=sheet, cols=1, rows=1)
            overwrite = True

        spreadsheet = worksheet.worksheet(sheet)

        if overwrite:
            spreadsheet.clear()

            # Upload Dataframe to Google Sheet
            set_with_dataframe(
                worksheet=spreadsheet,
                dataframe=df,
                row=row,
                col=column,
                include_column_header=header,
                resize=resize,
                allow_formulas=True,
                include_index=False,
                string_escaping="default")
        else:
            # append
            existing = get_as_dataframe(worksheet=spreadsheet)
            updated = existing.append(df)
            set_with_dataframe(spreadsheet, updated)
