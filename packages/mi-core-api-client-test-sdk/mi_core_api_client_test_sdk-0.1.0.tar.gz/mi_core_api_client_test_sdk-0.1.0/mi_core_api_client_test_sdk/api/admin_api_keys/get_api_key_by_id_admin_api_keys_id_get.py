from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_api_key_dto import ResponseWithMetadataSchemaAPIKeyDTO
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/admin/api-keys/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaAPIKeyDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Get Api Key By Id

     Retrieve an API key by its ID.

    This endpoint allows superusers to fetch the details of a specific API key by its ID.

    Args:
    - **id**: The ID of the API key.

    Returns:
    - **APIKeyDTO**: The details of the requested API key.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the API key with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Get Api Key By Id

     Retrieve an API key by its ID.

    This endpoint allows superusers to fetch the details of a specific API key by its ID.

    Args:
    - **id**: The ID of the API key.

    Returns:
    - **APIKeyDTO**: The details of the requested API key.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the API key with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Get Api Key By Id

     Retrieve an API key by its ID.

    This endpoint allows superusers to fetch the details of a specific API key by its ID.

    Args:
    - **id**: The ID of the API key.

    Returns:
    - **APIKeyDTO**: The details of the requested API key.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the API key with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Get Api Key By Id

     Retrieve an API key by its ID.

    This endpoint allows superusers to fetch the details of a specific API key by its ID.

    Args:
    - **id**: The ID of the API key.

    Returns:
    - **APIKeyDTO**: The details of the requested API key.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the API key with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
