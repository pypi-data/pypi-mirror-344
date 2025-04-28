"""
Main Artifact Scheduler module.

This module provides the main ArtifactScheduler class that coordinates scheduling
operations for Fabric artifacts (Notebooks, Dataflows, Pipelines) using the Fabric REST API.
"""
import io
from typing import Dict, List, Literal, Optional, Union

import sempy.fabric as fabric

from ._artifacts import ArtifactManager
from ._schedules import ScheduleManager, ScheduleValidator
from ._workspace import WorkspaceManager


class ArtifactScheduler:
    """Main class for scheduling Fabric artifacts.

    This class is the main entry point for scheduling operations. It coordinates
    workspace, artifact, and schedule management.

    :param workspace_id: Workspace ID to operate on, defaults to the current workspace.
    :param silent: If True, suppresses console output, defaults to True.
    """

    def __init__(self, workspace_id: Optional[str] = None, silent: bool = True):
        """Initialize the ArtifactScheduler.

        :param workspace_id: Workspace ID to operate on, defaults to the current workspace.
        :param silent: If True, suppresses console output, defaults to True.
        """
        self.silent = silent
        self.client = fabric.FabricRestClient()

        # Initialize managers with proper dependencies and configuration
        self.workspace_manager = WorkspaceManager(
            workspace_id=workspace_id, client=self.client, silent=silent
        )

        self.workspace_artifacts = self.workspace_manager.fetch_workspace_artifacts()

        self.artifact_manager = ArtifactManager(
            workspace_artifacts=self.workspace_artifacts, silent=silent
        )

        self.schedule_manager = ScheduleManager(
            client=self.client,
            workspace_id=self.workspace_manager.workspace_id,
            silent=silent,
        )

        # Set up validators
        self.schedule_validator = ScheduleValidator()

    def load_artifacts_from_csv(self, csv_source: Union[str, io.StringIO]) -> None:
        """Load artifacts to schedule from a CSV file or string.

        :param csv_source: Input can be:
            - CSV file path (string)
            - CSV content (string or StringIO)
        :raises ValueError: If CSV validation fails.
        """
        self.artifact_manager.set_artifacts_to_schedule(csv_source)

    def set_artifacts(self, artifacts: List[Dict]) -> None:
        """Set artifacts to schedule from a list of dictionaries.

        :param artifacts: List of artifact dictionaries to schedule.
        :raises ValueError: If validation fails.
        """
        self.artifact_manager.set_artifacts_to_schedule(artifacts)

    def display_schedules(self, scope: Literal["selected", "all"] = "selected") -> None:
        """Retrieve and display schedules for artifacts.

        This method fetches the latest schedules and displays them, ensuring
        that you always see the most up-to-date information.

        :param scope: Whether to display schedules for "selected" artifacts only
                    or for "all" artifacts in the workspace, defaults to "selected".
        :raises ValueError: If an invalid scope value is provided.
        """
        # Safety check for scope parameter to prevent typos leading to unintended behavior
        if scope not in ["selected", "all"]:
            raise ValueError(
                f"Invalid scope value: '{scope}'. Valid options are 'selected' or 'all'."
            )

        selected_only = scope == "selected"
        artifacts = (
            self.artifact_manager.artifacts_to_schedule
            if selected_only
            else self.workspace_artifacts
        )

        if selected_only and not artifacts:
            print(
                "No artifacts have been selected for scheduling. Use load_artifacts_from_csv() or set_artifacts() first."
            )
            return

        # Temporarily override silent mode for display_schedules
        original_silent = self.schedule_manager.silent
        self.schedule_manager.silent = False

        try:
            self.schedule_manager.display_schedules(artifacts)
        finally:
            # Restore original silent setting
            self.schedule_manager.silent = original_silent

    def delete_schedules(self, scope: Literal["selected", "all"] = "selected") -> None:
        """Delete schedules for artifacts.

        :param scope: Whether to delete schedules for "selected" artifacts only
                    or for "all" artifacts in the workspace, defaults to "selected".
        :raises ValueError: If an invalid scope value is provided.
        """
        # Safety check for scope parameter to prevent typos leading to unintended deletions
        if scope not in ["selected", "all"]:
            raise ValueError(
                f"Invalid scope value: '{scope}'. Valid options are 'selected' or 'all'."
            )

        selected_only = scope == "selected"
        artifacts = (
            self.artifact_manager.artifacts_to_schedule
            if selected_only
            else self.workspace_artifacts
        )

        if selected_only and not artifacts:
            print(
                "No artifacts have been selected for scheduling. Use load_artifacts_from_csv() or set_artifacts() first."
            )
            return

        # Delete the schedules
        self.schedule_manager.delete_schedules(artifacts)

    def create_schedules(self) -> None:
        """Create schedules for all selected artifacts.

        Note: Artifacts must first be loaded with load_artifacts_from_csv() or set_artifacts().
        """
        artifacts = self.artifact_manager.artifacts_to_schedule

        if not artifacts:
            print(
                "No artifacts have been selected for scheduling. Use load_artifacts_from_csv() or set_artifacts() first."
            )
            return

        # Create schedules - display is handled within this method
        self.schedule_manager.create_schedules(artifacts)
