"""
Constants for the Fabric Scheduler.

This module provides constants used throughout the fabric_scheduler package.
"""

__all__ = [
    "DEFAULT_TIMEZONE",
    "DEFAULT_START_TIME",
    "DEFAULT_END_TIME",
    "MAX_INTERVAL",
    "VALID_SCHEDULE_TYPES",
    "VALID_WEEKDAYS",
    "JOB_TYPES",
]

# Schedule Time Settings
DEFAULT_TIMEZONE = "Greenwich Standard Time"
"""Default timezone for schedules."""

DEFAULT_START_TIME = "00:00"
"""Default start time for schedules."""

DEFAULT_END_TIME = "23:59"
"""Default end time for schedules."""

MAX_INTERVAL = 5270400  # 10 years in minutes
"""Maximum allowed interval for cron schedules."""

# Valid Schedule Types and Values
VALID_SCHEDULE_TYPES = {"Cron", "Daily", "Weekly"}
"""Valid schedule types."""

VALID_WEEKDAYS = {
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
}
"""Valid weekdays for weekly schedules."""

# Artifact Job Types Mapping
JOB_TYPES = {
    "Notebook": "RunNotebook",
    "Dataflow": "Refresh",
    "DataPipeline": "Pipeline",
}
"""Mapping of artifact types to their corresponding job types."""
