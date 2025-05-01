from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_field_type import CustomFieldType
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_available_data_points import (
    ResponseWithMetadataSchemalistAvailableDataPoints,
)
from ...models.service_type import ServiceType
from ...types import UNSET, Response


def _get_kwargs(
    *,
    service_type: ServiceType,
    content_type: CustomFieldType,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_service_type = service_type.value
    params["service_type"] = json_service_type

    json_content_type = content_type.value
    params["content_type"] = json_content_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/custom-fields/data-points",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistAvailableDataPoints.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    service_type: ServiceType,
    content_type: CustomFieldType,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]:
    """Get Column Datapoints

     Get available data points for a custom column based on service and content type.

    Args:
    - **service_type**: The type of document (e.g. Youtube, Article or Reddit).
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **AvailableDataPoints**: A schema containing information about the available data points.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        service_type (ServiceType): Enumeration class representing service types.
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]
    """

    kwargs = _get_kwargs(
        service_type=service_type,
        content_type=content_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    service_type: ServiceType,
    content_type: CustomFieldType,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]:
    """Get Column Datapoints

     Get available data points for a custom column based on service and content type.

    Args:
    - **service_type**: The type of document (e.g. Youtube, Article or Reddit).
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **AvailableDataPoints**: A schema containing information about the available data points.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        service_type (ServiceType): Enumeration class representing service types.
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]
    """

    return sync_detailed(
        client=client,
        service_type=service_type,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    service_type: ServiceType,
    content_type: CustomFieldType,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]:
    """Get Column Datapoints

     Get available data points for a custom column based on service and content type.

    Args:
    - **service_type**: The type of document (e.g. Youtube, Article or Reddit).
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **AvailableDataPoints**: A schema containing information about the available data points.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        service_type (ServiceType): Enumeration class representing service types.
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]
    """

    kwargs = _get_kwargs(
        service_type=service_type,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    service_type: ServiceType,
    content_type: CustomFieldType,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]]:
    """Get Column Datapoints

     Get available data points for a custom column based on service and content type.

    Args:
    - **service_type**: The type of document (e.g. Youtube, Article or Reddit).
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **AvailableDataPoints**: A schema containing information about the available data points.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        service_type (ServiceType): Enumeration class representing service types.
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistAvailableDataPoints]
    """

    return (
        await asyncio_detailed(
            client=client,
            service_type=service_type,
            content_type=content_type,
        )
    ).parsed
