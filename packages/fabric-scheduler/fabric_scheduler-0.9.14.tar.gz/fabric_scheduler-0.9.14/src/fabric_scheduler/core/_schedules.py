"""
Schedule validation and management functionality.

This module handles schedule validation and API interactions for managing schedules.
"""
from typing import Any, Dict, List

from ..utils._api_utils import make_api_request
from ..utils._constants import (
    DEFAULT_END_TIME,
    DEFAULT_START_TIME,
    DEFAULT_TIMEZONE,
    JOB_TYPES,
    MAX_INTERVAL,
    VALID_SCHEDULE_TYPES,
    VALID_WEEKDAYS,
)
from ..utils._date_utils import is_valid_time_format, validate_date, validate_time
from ..utils._display_utils import (
    expand_nested_columns,
    format_dataframe_for_display,
    get_display_function,
)


class ScheduleValidator:
    """Validator for schedule configurations."""

    def validate_schedule_config(self, config: Dict) -> None:
        """Validate schedule configuration.

        :param config: Schedule config to validate.
        :raises ValueError: If validation fails.
        """
        self._validate_schedule_type(config)

        if config["type"] == "Cron":
            self._validate_cron_schedule(config)
        elif config["type"] == "Daily":
            self._validate_daily_schedule(config)
        elif config["type"] == "Weekly":
            self._validate_weekly_schedule(config)

        self._validate_optional_schedule_fields(config)

    def _validate_schedule_type(self, config: Dict) -> None:
        """Validate schedule type.

        :param config: Schedule config to validate.
        :raises ValueError: If type is invalid.
        """
        if "type" not in config:
            raise ValueError("Schedule type is required.")

        if config["type"] not in VALID_SCHEDULE_TYPES:
            raise ValueError(
                f"Invalid schedule type. Must be one of: {VALID_SCHEDULE_TYPES}"
            )

    def _validate_cron_schedule(self, config: Dict) -> None:
        """Validate cron schedule configuration.

        :param config: Schedule config to validate.
        :raises ValueError: If interval is invalid.
        """
        if "interval" not in config:
            raise ValueError("Interval is required for cron schedules.")

        if not (1 <= config["interval"] <= MAX_INTERVAL):
            raise ValueError(f"Interval must be between 1 and {MAX_INTERVAL}.")

    def _validate_daily_schedule(self, config: Dict) -> None:
        """Validate daily schedule configuration.

        :param config: Schedule config to validate.
        :raises ValueError: If times are invalid.
        """
        if "times" not in config:
            raise ValueError("Times are required for daily schedules.")

        if not all(is_valid_time_format(t) for t in config["times"]):
            raise ValueError("Times must be in HH:MM format.")

    def _validate_weekly_schedule(self, config: Dict) -> None:
        """Validate weekly schedule configuration.

        :param config: Schedule config to validate.
        :raises ValueError: If weekdays are invalid.
        """
        if "weekdays" not in config:
            raise ValueError("Weekdays are required for weekly schedules.")

        if len(config["weekdays"]) > 7:
            raise ValueError("Maximum 7 weekdays allowed.")

        if not all(day in VALID_WEEKDAYS for day in config["weekdays"]):
            raise ValueError(f"Weekdays must be one of: {VALID_WEEKDAYS}")

    def _validate_optional_schedule_fields(self, config: Dict) -> None:
        """Validate optional schedule fields if present.

        :param config: Schedule config to validate.
        :raises ValueError: If validation fails.
        """
        for field in ["startDate", "endDate"]:
            if field in config:
                validate_date(config[field])

        for field in ["startTime", "endTime"]:
            if field in config:
                validate_time(config[field])

        if "localTimeZone" in config and not isinstance(config["localTimeZone"], str):
            raise ValueError("Timezone must be a string.")


class ScheduleManager:
    """Manager for Fabric schedule operations.

    :param client: Fabric REST client.
    :param workspace_id: Workspace ID for the schedules.
    :param silent: Whether to suppress output.
    """

    def __init__(self, client: Any, workspace_id: str, silent: bool = True):
        """Initialize the schedule manager.

        :param client: Fabric REST client.
        :param workspace_id: Workspace ID for the schedules.
        :param silent: Whether to suppress output, defaults to True.
        """
        self.client = client
        self.workspace_id = workspace_id
        self.silent = silent

    def display_schedules(self, artifacts: List[Dict]) -> None:
        """Retrieve and display schedules for artifacts.

        This method combines the retrieval and display of schedules into a single operation,
        ensuring the most up-to-date schedules are always displayed.

        :param artifacts: List of artifacts to retrieve and display schedules for.
        :return: None
        """
        # First retrieve the latest schedules
        artifacts_with_schedules = self._fetch_schedules_for_artifacts(artifacts)

        # Then display them
        self._display_formatted_schedules(artifacts_with_schedules)

    def _fetch_schedules_for_artifacts(self, artifacts: List[Dict]) -> List[Dict]:
        """Retrieve schedules for all artifacts.

        :param artifacts: List of artifacts to retrieve schedules for.
        :return: List of artifacts with retrieved schedules.
        """
        for artifact in artifacts:
            if artifact.get("type") not in JOB_TYPES:
                continue

            try:
                artifact["retrieved_schedules"] = self._fetch_schedules_for_artifact(
                    artifact
                )
            except Exception as e:
                print(f"Error retrieving schedules for {artifact['displayName']}: {e}")

        return artifacts

    def _fetch_schedules_for_artifact(
        self, artifact: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Retrieve schedules for a single artifact.

        :param artifact: Artifact to retrieve schedules for.
        :return: List of schedule dictionaries.
        :raises FabricHTTPException: If API request fails.
        """
        job_type = self._get_job_type(artifact)
        url = f"/v1/workspaces/{self.workspace_id}/items/{artifact['id']}/jobs/{job_type}/schedules"

        response = make_api_request(self.client, "GET", url)

        # Explicitly cast the return value to the expected type
        schedules: List[Dict[str, Any]] = response.json().get("value", [])
        return schedules

    def _display_formatted_schedules(self, artifacts: List[Dict]) -> None:
        """Display formatted schedules for artifacts.

        :param artifacts: List of artifacts with retrieved schedules.
        """
        artifacts_with_schedules = [
            artifact
            for artifact in artifacts
            if artifact.get("retrieved_schedules", []) not in [None, []]
        ]

        if not artifacts_with_schedules:
            print("No artifacts found with schedules in current scope.")
            return

        try:
            display = get_display_function()

            if not self.silent:
                print("Schedules:")

            # Create a DataFrame for display
            columns_to_drop = ["schedule", "id", "description", "workspaceId"]
            df = format_dataframe_for_display(
                artifacts_with_schedules,
                columns_to_drop=columns_to_drop,
                rename_map={"type": "artifact_type"},
                explode_column="retrieved_schedules",
            )

            # Handle nested data if present
            if not df.empty:
                df = expand_nested_columns(df)

                # Rename id to avoid confusion
                if "id" in df.columns:
                    df.rename(columns={"id": "schedule_id"}, inplace=True)

                # Remove duplicates
                if "schedule_id" in df.columns:
                    df = df.drop_duplicates(subset=["schedule_id"])

            if self.silent:
                print(
                    f"Found {len(df) if not df.empty else 0} schedules across {len(artifacts_with_schedules)} artifacts"
                )
            else:
                display(df)
        except Exception:
            print(
                f"Error displaying schedules: {len(artifacts_with_schedules)} artifacts with schedules found"
            )

    def delete_schedules(self, artifacts: List[Dict]) -> bool:
        """Delete all schedules for artifacts.

        :param artifacts: List of artifacts to delete schedules for.
        :return: True if all schedules were deleted successfully.
        """
        # Count schedules before deletion for reporting
        self._fetch_schedules_for_artifacts(artifacts)
        schedules_before = sum(
            len(artifact.get("retrieved_schedules", [])) for artifact in artifacts
        )

        if schedules_before == 0:
            print("No schedules found to delete")
            return True

        print(f"Deleting {schedules_before} schedules...")

        # Delete schedules
        for artifact in artifacts:
            self._delete_schedules_for_artifact(artifact)

        # Verify deletion
        self._fetch_schedules_for_artifacts(artifacts)
        schedules_after = sum(
            len(artifact.get("retrieved_schedules", [])) for artifact in artifacts
        )

        if schedules_after == 0:
            print("All schedules deleted successfully")
            return True
        else:
            print(f"Warning: {schedules_after} schedule(s) could not be deleted")

            # Only show remaining schedules if deletion wasn't fully successful
            if not self.silent:
                self._display_formatted_schedules(artifacts)

        return schedules_after == 0

    def _delete_schedules_for_artifact(self, artifact: Dict) -> bool:
        """Delete all schedules for a single artifact.

        :param artifact: Artifact to delete schedules for.
        :return: True if successful.
        """
        for schedule in artifact.get("retrieved_schedules", []):
            try:
                self._delete_schedule(artifact, schedule["id"])
            except Exception as e:
                print(f"Error deleting schedule {schedule['id']}: {e}")
        return True

    def _delete_schedule(self, artifact: Dict, schedule_id: str) -> bool:
        """Delete a specific schedule for an artifact.

        :param artifact: Artifact containing the schedule.
        :param schedule_id: ID of the schedule to delete.
        :return: True if successful.
        :raises FabricHTTPException: If API request fails.
        """
        job_type = self._get_job_type(artifact)
        url = f"/v1/workspaces/{self.workspace_id}/items/{artifact['id']}/jobs/{job_type}/schedules/{schedule_id}"

        make_api_request(self.client, "DELETE", url)
        return True

    def create_schedules(self, artifacts: List[Dict]) -> List[Dict]:
        """Create schedules for all artifacts.

        :param artifacts: List of artifacts to schedule.
        :return: List of artifacts with updated schedule information.
        """
        print(f"Creating schedules for {len(artifacts)} artifacts...")
        success_count = 0
        failed_count = 0

        for artifact in artifacts:
            try:
                self._create_schedule(artifact)
                success_count += 1
            except Exception as e:
                print(f"Error creating schedule for {artifact['displayName']}: {e}")
                failed_count += 1

        # Refresh schedule information
        self._fetch_schedules_for_artifacts(artifacts)

        if failed_count == 0:
            print(f"Successfully created {success_count} schedules")
        else:
            print(f"Created {success_count} schedules, {failed_count} failed")

        # Display the schedules after creation
        self._display_formatted_schedules(artifacts)

        return artifacts

    def _create_schedule(self, artifact: Dict) -> bool:
        """Create a schedule for a single artifact.

        :param artifact: Artifact to create schedule for.
        :return: True if successful.
        :raises FabricHTTPException: If API request fails.
        :raises ValueError: If artifact type is unsupported.
        """
        job_type = self._get_job_type(artifact)
        schedule_body = self._build_schedule_body(artifact)

        url = f"/v1/workspaces/{self.workspace_id}/items/{artifact['id']}/jobs/{job_type}/schedules"
        make_api_request(
            self.client, "POST", url, json_data=schedule_body, expected_status=201
        )
        return True

    def _get_job_type(self, artifact: Dict) -> str:
        """Get job type for artifact with validation.

        :param artifact: Artifact to get job type for.
        :return: Corresponding job type.
        :raises ValueError: If artifact type is unsupported.
        """
        job_type = JOB_TYPES.get(artifact["type"])
        if not job_type:
            raise ValueError(f"Unsupported artifact type: {artifact['type']}")
        return job_type

    def _build_schedule_body(self, artifact: Dict) -> Dict:
        """Build schedule request body based on schedule type.

        :param artifact: Artifact containing schedule config.
        :return: Formatted request body.
        """
        schedule = artifact["schedule"]
        config = schedule["config"]

        base_body = {
            "enabled": schedule.get("enabled", True),
            "configuration": {
                "type": config["type"],
                "localTimeZoneId": config.get("localTimeZone", DEFAULT_TIMEZONE),
                "startDateTime": f"{config.get('startDate')}T{config.get('startTime', DEFAULT_START_TIME)}:00",
                "endDateTime": f"{config.get('endDate')}T{config.get('endTime', DEFAULT_END_TIME)}:00",
            },
        }

        # Add type-specific configuration
        if config["type"] == "Cron":
            base_body["configuration"]["interval"] = config["interval"]
        elif config["type"] == "Daily":
            base_body["configuration"]["times"] = config["times"]
        elif config["type"] == "Weekly":
            base_body["configuration"]["weekdays"] = config["weekdays"]
            base_body["configuration"]["times"] = config["times"]

        return base_body
