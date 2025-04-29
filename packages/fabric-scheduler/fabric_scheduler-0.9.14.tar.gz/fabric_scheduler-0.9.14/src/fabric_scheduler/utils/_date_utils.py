"""
Date and time utilities for the Fabric Scheduler.

This module provides utilities for date and time handling.
"""
from datetime import datetime
from typing import Optional

import pandas as pd

__all__ = [
    "parse_date",
    "parse_time",
    "is_valid_time_format",
    "validate_date",
    "validate_time",
    "get_current_date",
    "get_date_plus_year",
]


def parse_date(date_str: str) -> str:
    """Parse date string to YYYY-MM-DD format.

    :param date_str: Date string to parse.
    :return: Formatted date string.
    :raises ValueError: If parsing fails.
    """
    return pd.to_datetime(date_str).strftime("%Y-%m-%d")


def parse_time(time_str: str) -> str:
    """Parse time string to HH:MM format.

    :param time_str: Time string to parse.
    :return: Formatted time string.
    :raises ValueError: If parsing fails.
    """
    return pd.to_datetime(time_str, format="%H:%M").strftime("%H:%M")


def is_valid_time_format(time_str: str) -> bool:
    """Check if time string is in valid HH:MM format.

    :param time_str: Time string to check.
    :return: True if valid, False otherwise.
    """
    return (
        isinstance(time_str, str)
        and len(time_str) == 5
        and time_str[2] == ":"
        and time_str[:2].isdigit()
        and time_str[3:].isdigit()
    )


def validate_date(date_str: str) -> None:
    """Validate date string format.

    :param date_str: Date string to validate.
    :raises ValueError: If format is invalid.
    """
    try:
        pd.to_datetime(date_str)
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")


def validate_time(time_str: str) -> None:
    """Validate time string format.

    :param time_str: Time string to validate.
    :raises ValueError: If format is invalid.
    """
    try:
        pd.to_datetime(time_str, format="%H:%M")
    except ValueError:
        raise ValueError("Time must be in HH:MM format.")


def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format.

    :return: Current date string.
    """
    return datetime.now().strftime("%Y-%m-%d")


def get_date_plus_year(base_date: Optional[str] = None) -> str:
    """Get date one year from now or from specified base date.

    :param base_date: Optional base date string, defaults to current date.
    :return: Date string one year ahead.
    """
    if base_date:
        date = pd.to_datetime(base_date)
    else:
        date = pd.Timestamp.today()

    # Explicitly convert to string
    result: str = (date + pd.DateOffset(years=1)).strftime("%Y-%m-%d")
    return result
