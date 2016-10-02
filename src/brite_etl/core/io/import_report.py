from __future__ import division, absolute_import, print_function
import os
import xlwings as xw
import pandas as pd


def import_report(file_path, name, sheet, skip_rows=0):
    """Import a downloaded BriteCore report with proper formating.

    This lets you import a BriteCore .xls report as a dataframe without having
    to open it up, save policyId as text, etc. Please note that you MUST have
    Excel installed on your machine, because this opens the file up in Excel to read it.

    :param file_path: Path to directory containing file
    :type file_path: str
    :param name: Name of the file. Don't have to include dates, it will find the filename containing it.
    :type name: str
    :param sheet: Name (or index) of the sheet to grab
    :type sheet: str, int
    :param skip_rows: Number of rows to skip from beginning of sheet
    :type skip_rows: int
    :returns: The selected sheet as a dataframe with proper formatting
    :rtype: `Pandas.DataFrame`
    """

    # Search for a filename that contains the name they passed.
    # This gives users the ability to use the downloaded reports without having
    # to rename them and remove the dates and timestamps.
    files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    for f in files:
        if name in f:
            full_file = os.path.join(file_path, f)

    # This opens it up in Excel
    wb = xw.Book(full_file)
    ws = wb.sheets[sheet]

    table = ws.range('A1').offset(row_offset=skip_rows).expand(mode='table')

    # Convert the data into a pandas DataFrame
    df = table.options(pd.DataFrame, header=1).value

    return df
