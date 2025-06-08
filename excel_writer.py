# import polars as pl
# import pandas as pd
# from datetime import datetime
#
# df = pl.DataFrame({
#     "Name": ["Alice", "Bob", "Charlie"],
#     "Age": [25, 32, 29],
#     "City": ["New York", "Los Angeles", "Chicago"]
# })
#
# report_name = "Employee Report"
# version = "1.0"
# current_date = datetime.today().strftime("%Y-%m-%d")
#
# cover_data = {
#     "Field": ["Report Name", "Date", "Version"],
#     "Value": [report_name, current_date, version]
# }
# cover_df = pd.DataFrame(cover_data)
#
# df_pd = df.to_pandas()
#
# output_filename = "report.xlsx"
# with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
#     cover_df.to_excel(writer, sheet_name="Cover Sheet", index=False)
#     df_pd.to_excel(writer, sheet_name="Data", index=False)
#
# print(f"Excel file '{output_filename}' created with cover sheet and data.")




# VERSION 2

import polars as pl
from datetime import datetime
from xlsxwriter import Workbook


def create_report():
    # Sample Polars DataFrame
    df = pl.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 32, 29],
        "City": ["New York", "Los Angeles", "Chicago"]
    })

    df_meta = pl.DataFrame({
        "Name": ["Alice"],
        "Date": [datetime.today().strftime("%Y-%m-%d")],
        "Version": ["V1.0"]
    })

    with Workbook("report.xlsx") as wb:
        df_meta.write_excel(
            workbook=wb,
            worksheet="Cover Sheet",
        )
        df.write_excel(
            workbook=wb,
            worksheet="Calculation Results",
        )


if __name__ == "__main__":
    create_report()
