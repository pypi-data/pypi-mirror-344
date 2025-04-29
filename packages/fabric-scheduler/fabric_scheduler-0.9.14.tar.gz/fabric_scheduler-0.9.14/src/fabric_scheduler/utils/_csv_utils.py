"""
CSV utilities for the Fabric Scheduler.

This module provides utilities for CSV data handling.
"""
import io
from typing import Dict, List, Union

import pandas as pd

__all__ = [
    "is_csv_file_path",
    "read_csv_content",
    "read_csv_file",
    "read_csv_from_notebook_resource",
    "validate_csv_columns",
    "dataframe_to_dict_list",
]


def is_csv_file_path(input_str: str) -> bool:
    """Check if input string is a CSV file path.

    :param input_str: Input string to check.
    :return: True if input ends with .csv, False otherwise.
    """
    return isinstance(input_str, str) and input_str.endswith(".csv")


def read_csv_content(csv_content: Union[str, io.StringIO]) -> pd.DataFrame:
    """Read CSV content from string or file-like object.

    :param csv_content: CSV content to read.
    :return: DataFrame with CSV data.
    :raises ValueError: If CSV reading fails.
    """
    try:
        if isinstance(csv_content, str):
            csv_file = io.StringIO(csv_content)
        else:
            csv_file = csv_content

        return pd.read_csv(csv_file)
    except Exception as e:
        raise ValueError(f"Error parsing CSV content: {e}")


def read_csv_file(file_path: str) -> pd.DataFrame:
    """Read CSV file from specified path with error handling.

    :param file_path: Path to the CSV file.
    :return: DataFrame with CSV data.
    :raises ValueError: If file reading fails.
    """
    try:
        # First try to read directly
        return pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file '{file_path}': {e}")


def read_csv_from_notebook_resource(file_name: str) -> pd.DataFrame:
    """Read CSV file from notebook resources path.

    :param file_name: Name of the CSV file in the notebook resources.
    :return: DataFrame with CSV data.
    :raises ValueError: If file reading fails.
    """
    try:
        try:
            import notebookutils

            return pd.read_csv(f"{notebookutils.nbResPath}/builtin/{file_name}")
        except (ImportError, FileNotFoundError):
            # Fall back to normal file reading if notebookutils is not available
            # or the file is not in the notebook resources
            return read_csv_file(file_name)
    except Exception as e:
        raise ValueError(f"Error reading CSV from notebook resource '{file_name}': {e}")


def validate_csv_columns(df: pd.DataFrame, required_columns: List[str]) -> None:
    """Validate that DataFrame contains all required columns.

    :param df: DataFrame to validate.
    :param required_columns: List of required column names.
    :raises ValueError: If validation fails.
    """
    if df.empty:
        raise ValueError("CSV data is empty.")

    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns in CSV: {missing_columns}")


def dataframe_to_dict_list(df: pd.DataFrame) -> List[Dict]:
    """Convert DataFrame to list of dictionaries with proper handling of missing values.

    :param df: DataFrame to convert.
    :return: List of dictionaries.
    """
    return df.replace({pd.NA: None}).to_dict(orient="records")
