import click
import pandas as pd
import numpy as np
from pathlib import Path

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def inspect_file(file_path):
    """Inspect a CSV or Parquet file for data quality issues."""
    file_path = Path(file_path)

    try:
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.parquet':
            df = pd.read_parquet(file_path)
        else:
            click.echo(f"Error: Unsupported file format. Only CSV and Parquet files are supported.", err=True)
            return
    except Exception as e:
        click.echo(f"Error reading file: {str(e)}", err=True)
        return

    # Get basic information
    total_rows, total_columns = df.shape

    # Check for time series data
    potential_date_columns = df.apply(lambda x: pd.to_datetime(x, errors='coerce', infer_datetime_format=True).notna().sum())
    time_series = (potential_date_columns == total_rows).any()
    if time_series:
        index_column = potential_date_columns[potential_date_columns == total_rows].index[0]
        date_sample = df[index_column].iloc[0]
        click.echo(f"Detected time series column: {index_column}")
        click.echo(f"Sample date value: {date_sample}")
    else:
        index_column = "None"

    # Check for rows and columns with empty or null values
    null_counts_by_column = df.isnull().sum()
    null_counts_by_row = df.isnull().sum(axis=1)
    
    rows_with_nulls = null_counts_by_row[null_counts_by_row > 0]
    columns_with_nulls = null_counts_by_column[null_counts_by_column > 0]

    # Check for rows with many empty or null values
    null_threshold = 0.1  # 50% of columns are null
    rows_with_many_nulls = (null_counts_by_row > (total_columns * null_threshold)).sum()

    # Check for numerical outliers (using IQR method)
    numerical_columns = df.select_dtypes(include=[np.number]).columns
    outliers = 0
    for col in numerical_columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers += ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()

    # Check if the dataset is sparse or dense
    non_null_ratio = df.notna().sum().sum() / (total_rows * total_columns)
    sparsity = "Sparse" if non_null_ratio < 0.5 else "Dense"

    # Print results
    click.echo(f"Total rows: {total_rows}")
    click.echo(f"Total columns: {total_columns}")
    click.echo(f"Time series: {time_series}")
    click.echo(f"Index Column: {index_column}")
    click.echo(f"Rows with null values: {len(rows_with_nulls)}")
    click.echo(f"Columns with null values: {len(columns_with_nulls)}")
    if len(columns_with_nulls) > 0:
        click.echo("Columns with null values:")
        for col, count in columns_with_nulls.items():
            click.echo(f"  {col}: {count} null values")
    click.echo(f"Rows with many null values (>{null_threshold*100}% null): {rows_with_many_nulls}")
    click.echo(f"Rows with numerical outliers: {outliers}")
    click.echo(f"Sparse or Dense: {sparsity}")

if __name__ == "__main__":
    inspect_file()