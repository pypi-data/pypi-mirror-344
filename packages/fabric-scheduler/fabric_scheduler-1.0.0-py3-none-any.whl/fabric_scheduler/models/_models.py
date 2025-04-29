"""
Data models for the Fabric Scheduler.

This module contains the data model classes used in the fabric_scheduler package.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from ..utils._constants import DEFAULT_TIMEZONE


@dataclass
class ScheduleConfig:
    """Configuration for a schedule.

    :param schedule_type: The type of schedule (Cron/Daily/Weekly).
    :param local_time_zone: Timezone for the schedule.
    :param start_date: Start date in YYYY-MM-DD format.
    :param start_time: Start time in HH:MM format.
    :param end_date: End date in YYYY-MM-DD format.
    :param end_time: End time in HH:MM format.
    :param interval: Interval in minutes for cron jobs.
    :param times: List of times for daily/weekly schedules.
    :param weekdays: List of weekdays for weekly schedules.
    """

    schedule_type: str
    local_time_zone: str = DEFAULT_TIMEZONE
    start_date: Optional[str] = None
    start_time: Optional[str] = None
    end_date: Optional[str] = None
    end_time: Optional[str] = None
    interval: Optional[int] = None
    times: Optional[List[str]] = None
    weekdays: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the schedule config to a dictionary.

        :return: Dictionary representation of the schedule config.
        """
        result: Dict[str, Any] = {
            "type": self.schedule_type,
            "localTimeZone": self.local_time_zone,
        }

        # Add optional fields if set
        if self.start_date:
            result["startDate"] = self.start_date
        if self.start_time:
            result["startTime"] = self.start_time
        if self.end_date:
            result["endDate"] = self.end_date
        if self.end_time:
            result["endTime"] = self.end_time

        # Add type-specific fields
        if self.schedule_type == "Cron" and self.interval is not None:
            result["interval"] = self.interval
        elif self.schedule_type in ["Daily", "Weekly"] and self.times:
            result["times"] = self.times

        if self.schedule_type == "Weekly" and self.weekdays:
            result["weekdays"] = self.weekdays

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScheduleConfig":
        """Create a ScheduleConfig from a dictionary.

        :param data: Dictionary containing schedule configuration.
        :return: ScheduleConfig instance.
        """
        return cls(
            schedule_type=data.get("type", ""),
            local_time_zone=data.get("localTimeZone", DEFAULT_TIMEZONE),
            start_date=data.get("startDate"),
            start_time=data.get("startTime"),
            end_date=data.get("endDate"),
            end_time=data.get("endTime"),
            interval=data.get("interval"),
            times=data.get("times"),
            weekdays=data.get("weekdays"),
        )


@dataclass
class ArtifactSchedule:
    """Schedule for a Fabric artifact.

    :param enabled: Whether the schedule is enabled.
    :param config: Configuration for the schedule.
    """

    enabled: bool = True
    config: Optional[Union[ScheduleConfig, Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the artifact schedule to a dictionary.

        :return: Dictionary representation of the artifact schedule.
        """
        if isinstance(self.config, ScheduleConfig):
            config_dict = self.config.to_dict()
        else:
            config_dict = self.config or {}

        return {"enabled": self.enabled, "config": config_dict}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArtifactSchedule":
        """Create an ArtifactSchedule from a dictionary.

        :param data: Dictionary containing schedule data.
        :return: ArtifactSchedule instance.
        """
        config_data = data.get("config", {})
        config = ScheduleConfig.from_dict(config_data) if config_data else None

        return cls(enabled=data.get("enabled", True), config=config)


@dataclass
class Artifact:
    """Information about a Fabric artifact.

    :param id: Unique identifier of the artifact.
    :param display_name: Display name of the artifact.
    :param artifact_type: Type of the artifact (Notebook/Dataflow/Pipeline).
    :param description: Description of the artifact.
    :param workspace_id: Workspace ID containing the artifact.
    :param schedule: Schedule configuration.
    :param retrieved_schedules: List of retrieved schedules.
    """

    id: str
    display_name: str
    artifact_type: str
    description: str
    workspace_id: str
    schedule: Optional[Union[ArtifactSchedule, Dict[str, Any]]] = None
    retrieved_schedules: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the artifact to a dictionary.

        :return: Dictionary representation of the artifact.
        """
        if isinstance(self.schedule, ArtifactSchedule):
            schedule_dict = self.schedule.to_dict()
        else:
            schedule_dict = self.schedule or {}

        return {
            "id": self.id,
            "displayName": self.display_name,
            "type": self.artifact_type,
            "description": self.description,
            "workspaceId": self.workspace_id,
            "schedule": schedule_dict,
            "retrieved_schedules": self.retrieved_schedules or [],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Artifact":
        """Create an Artifact from a dictionary.

        :param data: Dictionary containing artifact data.
        :return: Artifact instance.
        """
        schedule_data = data.get("schedule", {})
        schedule = ArtifactSchedule.from_dict(schedule_data) if schedule_data else None

        return cls(
            id=data.get("id", ""),
            display_name=data.get("displayName", ""),
            artifact_type=data.get("type", ""),
            description=data.get("description", ""),
            workspace_id=data.get("workspaceId", ""),
            schedule=schedule,
            retrieved_schedules=data.get("retrieved_schedules", []),
        )
