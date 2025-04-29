"""
Display utilities for the Fabric Scheduler.

This module provides functions for displaying data consistently across the package.
"""
from typing import Any, Callable, Dict, List, Optional, cast

import pandas as pd

__all__ = [
    "print_if_not_silent",
    "get_display_function",
    "format_dataframe_for_display",
    "expand_nested_columns",
    "display_artifacts_as_table",
]


def print_if_not_silent(output: str, silent: bool = False) -> None:
    """Print output only if not in silent mode.

    :param output: String to print
    :param silent: Whether to suppress output
    """
    if not silent:
        print(output)


def get_display_function() -> Callable[..., None]:
    """Get the appropriate display function for the current environment.

    Attempts to use notebookutils display function, falls back to print if not available.

    :return: Display function to use
    """
    try:
        from notebookutils.visualization.display import display

        # Explicitly cast to proper type to avoid mypy errors
        return cast(Callable[..., None], display)
    except ImportError:
        # Mock display function if notebookutils is not available
        def simple_display(*args: Any, **kwargs: Any) -> None:
            """Placeholder for notebookutils display function."""
            for arg in args:
                if hasattr(arg, "shape"):  # For dataframes/series
                    print(f"DataFrame with shape {arg.shape}")
                    print(arg)
                else:
                    print(arg)

        return simple_display


def format_dataframe_for_display(
    data: List[Dict[str, Any]],
    columns_to_drop: Optional[List[str]] = None,
    rename_map: Optional[Dict[str, str]] = None,
    explode_column: Optional[str] = None,
) -> pd.DataFrame:
    """Format data as a pandas DataFrame for display.

    :param data: List of dictionaries to convert to DataFrame
    :param columns_to_drop: Optional list of columns to remove
    :param rename_map: Optional mapping of old column names to new ones
    :param explode_column: Optional column to explode (for nested lists)
    :return: Formatted DataFrame
    """
    if not data:
        return pd.DataFrame()

    # Create basic DataFrame
    df = pd.DataFrame(data)

    # Drop specified columns if they exist
    if columns_to_drop:
        existing_columns = [col for col in columns_to_drop if col in df.columns]
        if existing_columns:
            df = df.drop(existing_columns, axis=1)

    # Rename columns if specified
    if rename_map:
        df = df.rename(columns=rename_map)

    # Explode column if specified (for nested data)
    if explode_column and explode_column in df.columns:
        df = df.explode(explode_column).reset_index(drop=True)

        # If the exploded column contains dictionaries, expand them
        if (
            not df.empty
            and df[explode_column].apply(lambda x: isinstance(x, dict)).any()
        ):
            expanded_df = df[explode_column].apply(pd.Series)
            df = pd.concat([df.drop([explode_column], axis=1), expanded_df], axis=1)

    return df


def expand_nested_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Expand columns containing dictionaries into separate columns.

    :param df: DataFrame potentially containing nested dictionary columns
    :return: DataFrame with expanded columns
    """
    if df.empty:
        return df

    for column in df.columns:
        if df[column].apply(lambda x: isinstance(x, dict)).any():
            expanded_df = df[column].apply(pd.Series)

            # Prefix columns with original column name for clarity
            if column == "owner":
                # Use a pandas-compatible approach for column renaming
                prefix_dict = {col: f"owner_{col}" for col in expanded_df.columns}
                expanded_df = expanded_df.rename(columns=prefix_dict)

            df = pd.concat([df.drop([column], axis=1), expanded_df], axis=1)

    return df


def display_artifacts_as_table(
    artifacts: List[Dict[str, Any]], silent: bool = False, title: str = "Artifacts:"
) -> None:
    """Display a list of artifacts as a formatted table.

    :param artifacts: List of artifact dictionaries to display
    :param silent: Whether to suppress output
    :param title: Title to display above the table
    """
    if not artifacts:
        return

    if silent:
        print(f"{len(artifacts)} artifacts selected")
        return

    try:
        display = get_display_function()
        print(title)

        # Basic formatting
        df = format_dataframe_for_display(
            artifacts,
            columns_to_drop=["schedule", "id", "description", "workspaceId"],
            rename_map={"type": "artifact_type"},
        )

        display(df)
    except Exception:
        print(f"Unable to display artifact table: {len(artifacts)} artifacts found")
