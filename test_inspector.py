import pytest
from click.testing import CliRunner
from inspector import inspect_file
import pandas as pd
import numpy as np
from pathlib import Path

@pytest.fixture
def sample_csv(tmp_path):
  df = pd.DataFrame({
      'date': pd.date_range(start='2023-01-01', periods=100),
      'value': np.random.randn(100),
      'category': np.random.choice(['A', 'B', 'C', None], 100),
      'constant': 'X',
  })
  file_path = tmp_path / "sample.csv"
  df.to_csv(file_path, index=False)
  return file_path

@pytest.fixture
def sample_parquet(tmp_path):
  df = pd.DataFrame({
      'date': pd.date_range(start='2023-01-01', periods=100),
      'value': np.random.randn(100),
      'category': np.random.choice(['A', 'B', 'C', None], 100),
      'constant': 'X',
  })
  file_path = tmp_path / "sample.parquet"
  df.to_parquet(file_path, index=False)
  return file_path

def test_csv_file_inspection(sample_csv):
  runner = CliRunner()
  result = runner.invoke(inspect_file, [str(sample_csv)])
  assert result.exit_code == 0
  assert "Total rows: 100" in result.output
  assert "Total columns: 4" in result.output
  assert "Detected time series column: date" in result.output

def test_parquet_file_inspection(sample_parquet):
  runner = CliRunner()
  result = runner.invoke(inspect_file, [str(sample_parquet)])
  assert result.exit_code == 0
  assert "Total rows: 100" in result.output
  assert "Total columns: 4" in result.output
  assert "Detected time series column: date" in result.output

def test_unsupported_file_format(tmp_path):
  unsupported_file = tmp_path / "unsupported.txt"
  unsupported_file.write_text("This is an unsupported file format")
  runner = CliRunner()
  result = runner.invoke(inspect_file, [str(unsupported_file)])
  assert result.exit_code == 0
  assert "Error: Unsupported file format" in result.output

def test_null_value_detection(sample_csv):
  runner = CliRunner()
  result = runner.invoke(inspect_file, [str(sample_csv)])
  assert "Columns with null values:" in result.output
  assert "category:" in result.output

def test_numerical_outlier_detection(tmp_path):
  # Create a deterministic dataset with known outliers
  df = pd.DataFrame({
      'date': pd.date_range(start='2023-01-01', periods=100),
      'value': [1, 2, 3, 4, 5] * 20  # Regular values
  })
  # Add known outliers
  df.loc[0, 'value'] = 1000  # Upper outlier
  df.loc[1, 'value'] = -1000  # Lower outlier
  
  file_path = tmp_path / "outlier_sample.csv"
  df.to_csv(file_path, index=False)
  
  runner = CliRunner()
  result = runner.invoke(inspect_file, [str(file_path)])
  assert "Rows with numerical outliers: 2" in result.output

def test_sparse_dense_detection(tmp_path):
  dense_df = pd.DataFrame(np.random.choice([np.nan, 1], size=(100, 10), p=[0.1, 0.9]))
  dense_file = tmp_path / "dense.csv"
  dense_df.to_csv(dense_file, index=False)
  
  runner = CliRunner()
  dense_result = runner.invoke(inspect_file, [str(dense_file)])
  assert "Sparse or Dense: Dense" in dense_result.output

def test_sparse_detection(tmp_path):
  sparse_df = pd.DataFrame(np.random.choice([np.nan, 1], size=(100, 10), p=[0.9, 0.1]))
  sparse_file = tmp_path / "sparse.csv"
  sparse_df.to_csv(sparse_file, index=False)
  runner = CliRunner()
  sparse_result = runner.invoke(inspect_file, [str(sparse_file)])
  assert "Sparse or Dense: Sparse" in sparse_result.output


def test_nonexistent_file():
  runner = CliRunner()
  result = runner.invoke(inspect_file, ["nonexistent_file.csv"])
  assert result.exit_code == 2
  assert "Error: Invalid" in result.output
  assert "does not exist" in result.output