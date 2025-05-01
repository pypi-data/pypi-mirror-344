from tabulate import tabulate
import pandas as pd

def get_detailed(df):

    num_rows, num_cols = df.shape
    data = [
        ["Column Name", "Dtype", "Null", "Not Null", "Mean", "Unique Val"],
    ]

    null_counts = df.isnull().sum()
    total_counts = df.count()

    for col in df.columns:
        dtype = df[col].dtype
        null = null_counts.get(col, 0)
        not_null = total_counts.get(col, 0)
        mean_val = round(df[col].mean(), 2) if pd.api.types.is_numeric_dtype(dtype) else "-"
        unique_values = df[col].nunique()
        data.append([col, dtype, null, not_null, mean_val, unique_values])
    
    info = [
        ["Number of Rows", num_rows],
        ["Number of Rows", num_cols]
    ]

    return tabulate(info, headers=["Info", "Values"], tablefmt="rounded_outline") + "\n\n" + tabulate(data, headers="firstrow", tablefmt="rounded_outline")


