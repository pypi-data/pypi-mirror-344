import pandas as pd

def clean_missing_data(df, to_numeric=[None], to_datetime=[None], threshold_drop=0.4, drop_duplicates=False):
    """
    Cleans missing values in a DataFrame by:
    - Dropping columns with too many missing values.
    - Filling numeric columns with mean or median based on skewness.
    - Filling categorical columns with mode.
    - [Optional] Dropping duplicate rows.
    
    Parameters:
    - df: pandas DataFrame
    - threshold_drop: float, columns with missing % > this will be dropped

    Returns:
    - Cleaned DataFrame
    """
    df = df.copy()

    if drop_duplicates:
        df.drop_duplicates(inplace=True)
        print("\nDropped duplicate rows.")

    numeric_conversions = []
    datetime_conversions = []
    numeric_fillings = []
    categorical_fillings = []
    dropped_columns = []

    for col in to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            numeric_conversions.append(col)

    for col in to_datetime:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            datetime_conversions.append(col)

    missing_info = df.isnull().mean()

    for col in df.columns:
        missing_ratio = missing_info[col]
        
        if missing_ratio == 0:
            continue
        
        if missing_ratio > threshold_drop:
            dropped_columns.append((col, f"{missing_ratio:.2%}"))
            df.drop(columns=[col], inplace=True)
            continue

        if df[col].dtype in ['float64', 'int64']:
            if abs(df[col].skew()) < 1:
                fill_value = df[col].mean()
                method = 'mean'
            else:
                fill_value = df[col].median()
                method = 'median'
            df[col] = df[col].fillna(fill_value)
            numeric_fillings.append((col, method))
        else:
            mode_value = df[col].mode()
            if not mode_value.empty:
                df[col] = df[col].fillna(mode_value[0])
                categorical_fillings.append((col, 'mode'))
            else:
                df[col] = df[col].fillna('Unknown')
                categorical_fillings.append((col, 'Unknown'))


    if numeric_conversions:
        print("Converting columns to numeric:")
        for col in numeric_conversions:
            print(f"    • {col}")
    
    if datetime_conversions:
        print("\nConverting columns to datetime:")
        for col in datetime_conversions:
            print(f"    • {col}")

    if numeric_fillings:
        print("\nFilling numeric columns:")
        for col, method in numeric_fillings:
            print(f"    • {col:<16} → {method}")

    if categorical_fillings:
        print("\nFilling categorical columns:")
        for col, method in categorical_fillings:
            print(f"    • {col:<16} → {method}")

    if dropped_columns:
        print("\nDropping columns due to high missing values:")
        for col, ratio in dropped_columns:
            print(f"    • {col:<16} → {ratio} missing")

    return df
