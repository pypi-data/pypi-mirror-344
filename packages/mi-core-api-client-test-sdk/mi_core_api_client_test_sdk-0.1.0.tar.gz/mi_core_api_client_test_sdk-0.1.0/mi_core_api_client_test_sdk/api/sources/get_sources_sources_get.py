from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_paginated_response_source_get_schema import (
    ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["per_page"] = per_page

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sources",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]:
    """Get Sources

     Get a list of sources for a logged-in user.

    This endpoint retrieves sources for a logged-in user.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[SourceGetSchema]**: A paginated response containing source information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        q=q,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]:
    """Get Sources

     Get a list of sources for a logged-in user.

    This endpoint retrieves sources for a logged-in user.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[SourceGetSchema]**: A paginated response containing source information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]
    """

    return sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        q=q,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]:
    """Get Sources

     Get a list of sources for a logged-in user.

    This endpoint retrieves sources for a logged-in user.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[SourceGetSchema]**: A paginated response containing source information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        q=q,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]]:
    """Get Sources

     Get a list of sources for a logged-in user.

    This endpoint retrieves sources for a logged-in user.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[SourceGetSchema]**: A paginated response containing source information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseSourceGetSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            per_page=per_page,
            q=q,
        )
    ).parsed
