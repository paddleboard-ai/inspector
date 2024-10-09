# Data Inspector CLI Tool

The Data Inspector CLI Tool is a command-line utility designed to quickly analyze CSV and Parquet files for data quality issues. It provides insights into the structure and content of your datasets, helping you identify potential problems and characteristics of your data before you dive in.

## Features

- Supports CSV and Parquet file formats
- Provides basic file information (total rows and columns)
- Detects time series data and identifies the index column
- Identifies rows and columns with null values
- Detects rows with a high percentage of null values
- Identifies numerical outliers using the Interquartile Range (IQR) method
- Determines if the dataset is sparse or dense

## Focus and caveats

- It has one and only one use case: for the developer/data scientist/data engineer to get a quick read of the data before they delve into it
- The focus of this tool is fast feedback about local, flat file data sets.
- Zero configuration. Not even command line flags =)
- Minimal set of essential metrics about a dataset
- Only csv and parquet files are supported
- This tool is _not_ meant to replace comprehensive data quality tools like Soda, dbt tests, GX, Monte Carlo, etc.
- Not intended to be used in data or CI pipelines.

## Installation

To install the Data Inspector CLI Tool, follow these steps:

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Run the following command to install the tool:

```
pip install .
```

This will install the Data Inspector CLI Tool and its dependencies.

## Usage

After installation, you can use the Data Inspector CLI Tool from the command line as follows:

```
inspector <path_to_your_file>
```

Replace `<path_to_your_file>` with the path to the CSV or Parquet file you want to inspect.

For example:

```
inspector data/my_dataset.csv
```

or

```
inspector data/my_dataset.parquet
```

## Output

The tool will provide the following information about your dataset:

- Total number of rows and columns
- Whether the dataset is a time series and the identified index column (if applicable)
- Number of rows and columns with null values
- Detailed list of columns with null values and their respective counts
- Number of rows with a high percentage of null values
- Number of rows with numerical outliers
- Whether the dataset is considered sparse or dense

```
$ inspector my_data_example.csv 
Detected time series column: LVLDATE
Sample date value: 2024-05-05
Total rows: 80
Total columns: 11
Time series: True
Index Column: LVLDATE
Rows with null values: 4
Columns with null values: 3
Columns with null values:
  SUPP2: 2 null values
  SUPP4: 1 null values
  RES2: 1 null values
Rows with many null values (>10.0% null): 0
Rows with numerical outliers: 1
Sparse or Dense: Dense
```

## Requirements

- Python 3.6+
- Click
- pandas
- numpy

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the development dependencies:
   ```
   pip install -e .
   ```

## Testing

To run the unit tests:

1. `pip install pytest`
2. `pytest test_inspector.py`

## Contributing

Contributions to the Data Inspector CLI Tool are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache 2.0 license.
