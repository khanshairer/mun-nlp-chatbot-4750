import pandas as pd

EXCEL_PATH = "data/all_faculty_full_combined.xlsx"

df = pd.read_excel(EXCEL_PATH)
print(df.columns.tolist())
