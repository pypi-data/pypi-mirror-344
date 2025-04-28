"""
Workspace management functionality.

This module handles workspace-related operations, including initialization and artifact retrieval.
"""
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import sempy.fabric as fabric

from ..utils._api_utils import (
    extract_required_fields,
    make_api_request,
    validate_response_items,
)
from ..utils._display_utils import get_display_function, print_if_not_silent


class WorkspaceManager:
    """Manager for Fabric workspace operations.

    :param workspace_id: ID of the workspace to manage.
    :param client: Fabric REST client.
    :param silent: Whether to suppress output.
    """

    def __init__(
        self,
        workspace_id: Optional[str] = None,
        client: Any = None,
        silent: bool = True,
    ):
        """Initialize the workspace manager.

        :param workspace_id: ID of the workspace to manage, defaults to None.
        :param client: Fabric REST client, defaults to None.
        :param silent: Whether to suppress output, defaults to True.
        """
        self.silent = silent
        self.client = client or fabric.FabricRestClient()
        self.workspace_id, self.workspace_name = self._initialize_workspace(
            workspace_id
        )

    def _initialize_workspace(self, workspace_id: Optional[str]) -> Tuple[str, str]:
        """Initialize the workspace by resolving its ID and name.

        :param workspace_id: Workspace ID to initialize. If None, the current workspace is used.
        :return: Tuple of (workspace_id, workspace_name).
        :raises WorkspaceNotFoundException: If workspace can't be found.
        """
        workspace_id = workspace_id or fabric.get_workspace_id()
        workspace_name = self._resolve_workspace_name(workspace_id)

        print_if_not_silent(
            f"Workspace: {workspace_name} ({workspace_id})", self.silent
        )

        return workspace_id, workspace_name

    def _resolve_workspace_name(self, workspace_id: str) -> str:
        """Resolve workspace name from ID.

        :param workspace_id: Workspace ID to resolve.
        :return: Workspace name.
        :raises WorkspaceNotFoundException: If workspace can't be found.
        """
        try:
            response = self.client.get(f"/v1/workspaces/{workspace_id}")
            data = response.json()
            # Explicitly specify return type
            workspace_name: str = data.get("displayName", f"Workspace {workspace_id}")
            return workspace_name
        except Exception as e:
            print(f"Error resolving workspace name: {e}")
            raise

    def fetch_workspace_artifacts(self) -> List[Dict[str, Any]]:
        """Fetch all artifacts from the workspace.

        :return: List of artifacts in the workspace.
        :raises Exception: If artifact fetching fails.
        """
        try:
            response = self._get_artifacts_from_api()
            artifacts = self._process_artifacts_response(response)

            if not self.silent:
                print(f"Items found in workspace: {len(artifacts)}")
                display = get_display_function()
                display(pd.DataFrame(artifacts))

            return artifacts
        except Exception as e:
            print(f"Error fetching artifacts: {e}")
            return []

    def _get_artifacts_from_api(self) -> Dict[str, Any]:
        """Get artifacts from API.

        :return: API response containing artifacts.
        :raises FabricHTTPException: If API request fails.
        """
        url = f"/v1/workspaces/{self.workspace_id}/items"
        response = make_api_request(self.client, "GET", url)
        # Explicitly specify return type
        result: Dict[str, Any] = response.json()
        return result

    def _process_artifacts_response(
        self, response: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Process artifacts response from API.

        :param response: API response to process.
        :return: List of processed artifacts.
        :raises ValueError: If required fields are missing.
        """
        artifacts = response.get("value", [])
        required_fields = {"id", "type", "displayName", "description", "workspaceId"}

        validate_response_items(artifacts, list(required_fields), "artifacts")

        return [
            extract_required_fields(
                artifact,
                list(required_fields),
                f"artifact '{artifact.get('displayName', 'unknown')}'",
            )
            for artifact in artifacts
        ]
