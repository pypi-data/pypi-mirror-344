
def clean_column_names(df):

    """
    Cleans and standardizes the column names of a Pandas DataFrame by:
        - Stripping leading and trailing whitespace
        - Converting all names to lowercase
        - Replacing spaces with underscores

    Returns:
        pd.DataFrame: A new DataFrame with cleaned and standardized column names.
    """

    df = df.copy()
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')

    return df

