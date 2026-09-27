import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
data_path = project_folder / "data" / "Telco-Customer-Churn.csv"

data = pd.read_csv(data_path)


print("\nColumn names:")
print(data.columns)

print("\nMissing values:")
print(data.isnull().sum())

print("\nDuplicate rows:")
print(data.duplicated().sum())

print("\nChurn distribution:")
print(data["Churn"].value_counts())

print("\nData types:")
print(data.dtypes)

print("\nUnique values:")
print(data.nunique())