"""
Artifact management functionality.

This module handles artifact processing, matching and validation.
"""
import io
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ..utils._constants import DEFAULT_END_TIME, DEFAULT_START_TIME, DEFAULT_TIMEZONE
from ..utils._csv_utils import (
    is_csv_file_path,
    read_csv_content,
    read_csv_from_notebook_resource,
    validate_csv_columns,
)
from ..utils._date_utils import (
    get_current_date,
    get_date_plus_year,
    parse_date,
    parse_time,
)
from ..utils._display_utils import display_artifacts_as_table


class ArtifactManager:
    """Manager for Fabric artifacts operations.

    :param workspace_artifacts: List of artifacts in the workspace.
    :param silent: Whether to suppress output.
    """

    def __init__(self, workspace_artifacts: List[Dict], silent: bool = True):
        """Initialize the artifact manager.

        :param workspace_artifacts: List of artifacts in the workspace.
        :param silent: Whether to suppress output, defaults to True.
        """
        self.workspace_artifacts = workspace_artifacts
        self.silent = silent
        self.artifacts_to_schedule: List[Dict] = []

    def set_artifacts_to_schedule(
        self, artifacts_to_schedule: Union[List[Dict], str, io.StringIO]
    ) -> List[Dict]:
        """Set artifacts to schedule from multiple input types.

        :param artifacts_to_schedule: Input can be:
            - List of dictionaries
            - CSV file path (string)
            - CSV content (string or StringIO)
        :return: List of artifacts ready to be scheduled.
        :raises ValueError: If input validation fails.
        """
        artifacts = self._parse_input(artifacts_to_schedule)
        populated_artifacts = self._populate_artifact_properties(artifacts)
        matched_artifacts = self._match_artifacts(populated_artifacts)

        self.artifacts_to_schedule = matched_artifacts
        display_artifacts_as_table(
            self.artifacts_to_schedule, self.silent, "Artifacts to be scheduled:"
        )

        return self.artifacts_to_schedule

    def _parse_input(
        self, input_data: Union[List[Dict], str, io.StringIO]
    ) -> List[Dict]:
        """Parse input data into artifact dictionaries.

        :param input_data: Input to parse.
        :return: List of artifact dictionaries.
        :raises ValueError: If parsing fails.
        """
        if isinstance(input_data, list):
            return input_data
        elif isinstance(input_data, (str, io.StringIO)):
            return self._parse_csv_input(input_data)
        else:
            raise ValueError(f"Unsupported input type: {type(input_data)}")

    def _parse_csv_input(self, csv_input: Union[str, io.StringIO]) -> List[Dict]:
        """Parse CSV input data.

        :param csv_input: CSV data as string, path, or StringIO.
        :return: List of artifact dictionaries.
        :raises ValueError: If parsing fails.
        """
        try:
            if isinstance(csv_input, str) and is_csv_file_path(csv_input):
                df = read_csv_from_notebook_resource(csv_input)
            else:
                df = read_csv_content(csv_input)

            return self._process_csv_dataframe(df)
        except Exception as e:
            raise ValueError(f"Error processing CSV input: {e}")

    def _process_csv_dataframe(self, df: pd.DataFrame) -> List[Dict]:
        """Process CSV data into artifact dictionaries.

        :param df: DataFrame containing schedule data.
        :return: List of processed artifact dictionaries.
        :raises ValueError: If required columns are missing.
        """
        required_columns = {
            "displayName",
            "type",
            "enabled",
            "schedule type",
            "localTimeZone",
            "startDate",
            "startTime",
            "endDate",
            "endTime",
            "interval",
            "times",
            "weekdays",
        }

        validate_csv_columns(df, list(required_columns))

        return [self._create_artifact_from_row(row) for _, row in df.iterrows()]

    def _create_artifact_from_row(self, row: pd.Series) -> Dict:
        """Create artifact dict from CSV row.

        :param row: Single row from CSV data.
        :return: Artifact dictionary with schedule config.
        """
        return {
            "displayName": row["displayName"],
            "type": row["type"] if pd.notna(row["type"]) else None,
            "schedule": {
                "enabled": bool(row["enabled"]) if pd.notna(row["enabled"]) else None,
                "config": self._create_schedule_config_from_row(row),
            },
        }

    def _create_schedule_config_from_row(self, row: pd.Series) -> Dict:
        """Create schedule config from CSV row.

        :param row: Single row from CSV data.
        :return: Schedule configuration dictionary.
        """
        config: Dict[str, Any] = {}

        # Handle schedule type
        if pd.notna(row["schedule type"]):
            config["type"] = str(row["schedule type"])

        # Handle timezone
        if pd.notna(row["localTimeZone"]):
            config["localTimeZone"] = str(row["localTimeZone"])

        # Handle dates with proper string conversion to fix type errors
        if pd.notna(row["startDate"]):
            config["startDate"] = parse_date(str(row["startDate"]))

        if pd.notna(row["startTime"]):
            config["startTime"] = parse_time(str(row["startTime"]))

        if pd.notna(row["endDate"]):
            config["endDate"] = parse_date(str(row["endDate"]))

        if pd.notna(row["endTime"]):
            config["endTime"] = parse_time(str(row["endTime"]))

        # Handle interval as int
        if pd.notna(row.get("interval")):
            config["interval"] = int(row["interval"])

        # Handle lists with safe null checking
        if pd.notna(row.get("times")) and row.get("times") is not None:
            times_str = str(row.get("times", ""))
            config["times"] = times_str.split(",")
        else:
            config["times"] = []

        if pd.notna(row.get("weekdays")) and row.get("weekdays") is not None:
            weekdays_str = str(row.get("weekdays", ""))
            config["weekdays"] = weekdays_str.split(",")
        else:
            config["weekdays"] = []

        return {k: v for k, v in config.items() if v is not None}

    def _populate_artifact_properties(self, artifacts: List[Dict]) -> List[Dict]:
        """Validate and populate artifact properties.

        :param artifacts: List of artifacts to process.
        :return: List of validated artifacts.
        """
        validator = ArtifactValidator()
        return [
            validator.validate_and_populate_props(artifact) for artifact in artifacts
        ]

    def _match_artifacts(self, artifacts: List[Dict]) -> List[Dict]:
        """Match user-provided artifacts with workspace artifacts.

        :param artifacts: List of artifacts to match.
        :return: List of matched artifacts.
        """
        matcher = ArtifactMatcher(self.workspace_artifacts)
        matched = []
        skipped = 0

        for artifact in artifacts:
            try:
                matched.append(matcher.find_matching_artifact(artifact))
            except ValueError as e:
                if not self.silent:
                    print(f"Skipping artifact: {e}")
                skipped += 1

        if skipped > 0 and self.silent:
            print(f"Skipped {skipped} artifact(s) that could not be matched")

        return matched


class ArtifactMatcher:
    """Matcher for finding artifacts in workspace inventory.

    :param workspace_artifacts: List of artifacts in the workspace.
    """

    def __init__(self, workspace_artifacts: List[Dict]):
        """Initialize the artifact matcher.

        :param workspace_artifacts: List of artifacts in the workspace.
        """
        self.workspace_artifacts = workspace_artifacts

    def find_matching_artifact(self, artifact: Dict) -> Dict:
        """Find matching artifact in workspace.

        :param artifact: Artifact to match.
        :return: Matched artifact with full properties.
        :raises ValueError: If no matching artifact found.
        """
        display_name = artifact["displayName"]
        artifact_type = artifact.get("type")

        matches = self._find_artifacts_by_name(display_name)

        if not matches:
            raise ValueError(f"No matching artifact found for {display_name}")

        if len(matches) > 1:
            matches = self._filter_by_type_if_needed(matches, artifact_type)

        if not matches:
            raise ValueError(
                f"No matching artifact found for {display_name} with type {artifact_type}"
            )

        return self._merge_artifact_properties(artifact, matches[0])

    def _find_artifacts_by_name(self, display_name: str) -> List[Dict]:
        """Find artifacts by display name.

        :param display_name: Name to search for.
        :return: List of matching artifacts.
        """
        return [
            item
            for item in self.workspace_artifacts
            if item["displayName"] == display_name
        ]

    def _filter_by_type_if_needed(
        self, artifacts: List[Dict], artifact_type: Optional[str]
    ) -> List[Dict]:
        """Filter artifacts by type if needed.

        :param artifacts: List of artifacts to filter.
        :param artifact_type: Type to filter by.
        :return: Filtered list of artifacts.
        :raises ValueError: If multiple artifacts found without type specified.
        """
        if len(artifacts) > 1 and not artifact_type:
            raise ValueError(
                f"Multiple artifacts found with name '{artifacts[0]['displayName']}'. "
                "Please specify type."
            )
        return [
            item
            for item in artifacts
            if not artifact_type or item["type"] == artifact_type
        ]

    def _merge_artifact_properties(
        self, user_artifact: Dict, matched_artifact: Dict
    ) -> Dict:
        """Merge user-provided and matched artifact properties.

        :param user_artifact: User-provided artifact data.
        :param matched_artifact: Matched workspace artifact.
        :return: Merged artifact dictionary.
        """
        return {
            **user_artifact,
            "id": matched_artifact["id"],
            "type": matched_artifact["type"],
            "description": matched_artifact["description"],
            "workspaceId": matched_artifact["workspaceId"],
        }


class ArtifactValidator:
    """Validator for artifact properties."""

    def validate_and_populate_props(self, artifact: Dict) -> Dict:
        """Validate and populate artifact schedule properties.

        :param artifact: Artifact to validate.
        :return: Validated artifact with defaults populated.
        :raises ValueError: If validation fails.
        """
        self._validate_artifact_structure(artifact)

        # We don't need to validate schedule config here as that's done by ScheduleValidator
        # in the schedules module when the schedule is created

        return self._apply_default_schedule_values(artifact)

    def _validate_artifact_structure(self, artifact: Dict) -> None:
        """Validate basic artifact structure.

        :param artifact: Artifact to validate.
        :raises ValueError: If required keys are missing.
        """
        if not isinstance(artifact, dict):
            raise ValueError("Artifact must be a dictionary.")

        required = {"displayName", "schedule"}
        if not required.issubset(artifact.keys()):
            missing = required - set(artifact.keys())
            raise ValueError(f"Missing required keys: {missing}")

        if "config" not in artifact["schedule"]:
            raise ValueError("Schedule config is required.")

    def _apply_default_schedule_values(self, artifact: Dict) -> Dict:
        """Apply default values to schedule configuration.

        :param artifact: Artifact to process.
        :return: Artifact with defaults populated.
        """
        artifact["type"] = artifact.get("type") or None

        schedule = artifact["schedule"]
        # If the "enabled" field in the CSV is left blank, schedule.get("enabled", True)
        # may return an empty string ("") because the property exists in the dictionary
        # but has no value. To handle this, we first retrieve its value and then set it
        # to True if it is empty or None. This ensures that the schedule is enabled by
        # default when not explicitly specified.
        schedule["enabled"] = schedule.get("enabled") or True

        config = schedule["config"]
        today = get_current_date()
        next_year = get_date_plus_year()

        config["startDate"] = config.get("startDate") or today
        config["startTime"] = config.get("startTime") or DEFAULT_START_TIME
        config["endDate"] = config.get("endDate") or next_year
        config["endTime"] = config.get("endTime") or DEFAULT_END_TIME
        config["localTimeZone"] = config.get("localTimeZone") or DEFAULT_TIMEZONE

        return artifact
