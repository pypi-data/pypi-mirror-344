"""
API utilities for the Fabric Scheduler.

This module provides utilities for making API requests and handling responses
consistently across the package.
"""
from typing import Any, Dict, List, Optional

from sempy.fabric.exceptions import FabricHTTPException

__all__ = ["make_api_request", "extract_required_fields", "validate_response_items"]


def make_api_request(
    client: Any,
    method: str,
    url: str,
    json_data: Optional[Dict] = None,
    expected_status: int = 200,
) -> Any:
    """Make an API request to the Fabric REST API with consistent error handling.

    :param client: Fabric REST client
    :param method: HTTP method (GET, POST, DELETE, etc.)
    :param url: API endpoint URL
    :param json_data: Optional JSON data for request body
    :param expected_status: Expected HTTP status code for success
    :return: Response object
    :raises FabricHTTPException: If API request fails
    """
    if method == "GET":
        response = client.get(url)
    elif method == "POST":
        response = client.post(url, json=json_data)
    elif method == "DELETE":
        response = client.delete(url)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    if response.status_code != expected_status:
        raise FabricHTTPException(response)

    return response


def extract_required_fields(
    data: Dict, required_fields: List[str], display_name: Optional[str] = None
) -> Dict:
    """Extract required fields from a dictionary with validation.

    :param data: Source dictionary
    :param required_fields: List of required field names
    :param display_name: Optional name for error messages
    :return: Dictionary containing only the required fields
    :raises ValueError: If any required fields are missing
    """
    missing_fields = set(required_fields) - set(data.keys())
    if missing_fields:
        error_context = f" in {display_name}" if display_name else ""
        raise ValueError(f"Missing required fields{error_context}: {missing_fields}")

    return {field: data.get(field) for field in required_fields}


def validate_response_items(
    items: List[Dict], required_fields: List[str], item_type: str = "items"
) -> None:
    """Validate that each item in a response contains required fields.

    :param items: List of items to validate
    :param required_fields: Required fields each item should have
    :param item_type: Description of items for error messages
    :raises ValueError: If validation fails
    """
    if not items:
        raise ValueError(f"No {item_type} found in response.")

    for i, item in enumerate(items):
        missing = set(required_fields) - set(item.keys())
        if missing:
            raise ValueError(f"Missing required fields in {item_type}[{i}]: {missing}")
