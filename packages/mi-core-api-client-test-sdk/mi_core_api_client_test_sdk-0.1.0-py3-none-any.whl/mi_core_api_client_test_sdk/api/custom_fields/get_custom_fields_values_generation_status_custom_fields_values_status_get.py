from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_custom_field_values_progress_info import (
    ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo,
)
from ...types import UNSET, Response


def _get_kwargs(
    *,
    custom_field_ids: list[UUID],
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_custom_field_ids = []
    for custom_field_ids_item_data in custom_field_ids:
        custom_field_ids_item = str(custom_field_ids_item_data)
        json_custom_field_ids.append(custom_field_ids_item)

    params["custom_field_ids"] = json_custom_field_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/custom-fields/values/status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    custom_field_ids: list[UUID],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]:
    """Get Custom Fields Values Generation Status

     Retrieve the current progress of custom field values generation.

    This endpoint returns the generation status of values for the provided custom field IDs.
    Progress can be partially cached in memory, and any missing progress data will be fetched from the
    database.

    Args:
    - **custom_field_ids**: List of UUIDs of custom fields to retrieve status for.

    Returns:
    - **list[CustomFieldValuesProgressInfo]**: List of progress info for each requested custom field.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        custom_field_ids (list[UUID]): List of custom fields IDs to check values generation for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]
    """

    kwargs = _get_kwargs(
        custom_field_ids=custom_field_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    custom_field_ids: list[UUID],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]:
    """Get Custom Fields Values Generation Status

     Retrieve the current progress of custom field values generation.

    This endpoint returns the generation status of values for the provided custom field IDs.
    Progress can be partially cached in memory, and any missing progress data will be fetched from the
    database.

    Args:
    - **custom_field_ids**: List of UUIDs of custom fields to retrieve status for.

    Returns:
    - **list[CustomFieldValuesProgressInfo]**: List of progress info for each requested custom field.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        custom_field_ids (list[UUID]): List of custom fields IDs to check values generation for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]
    """

    return sync_detailed(
        client=client,
        custom_field_ids=custom_field_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    custom_field_ids: list[UUID],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]:
    """Get Custom Fields Values Generation Status

     Retrieve the current progress of custom field values generation.

    This endpoint returns the generation status of values for the provided custom field IDs.
    Progress can be partially cached in memory, and any missing progress data will be fetched from the
    database.

    Args:
    - **custom_field_ids**: List of UUIDs of custom fields to retrieve status for.

    Returns:
    - **list[CustomFieldValuesProgressInfo]**: List of progress info for each requested custom field.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        custom_field_ids (list[UUID]): List of custom fields IDs to check values generation for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]
    """

    kwargs = _get_kwargs(
        custom_field_ids=custom_field_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    custom_field_ids: list[UUID],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]]:
    """Get Custom Fields Values Generation Status

     Retrieve the current progress of custom field values generation.

    This endpoint returns the generation status of values for the provided custom field IDs.
    Progress can be partially cached in memory, and any missing progress data will be fetched from the
    database.

    Args:
    - **custom_field_ids**: List of UUIDs of custom fields to retrieve status for.

    Returns:
    - **list[CustomFieldValuesProgressInfo]**: List of progress info for each requested custom field.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        custom_field_ids (list[UUID]): List of custom fields IDs to check values generation for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistCustomFieldValuesProgressInfo]
    """

    return (
        await asyncio_detailed(
            client=client,
            custom_field_ids=custom_field_ids,
        )
    ).parsed
