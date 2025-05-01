from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_paginated_response_collection_dto import (
    ResponseWithMetadataSchemaPaginatedResponseCollectionDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_collection_name: Union[None, Unset, str]
    if isinstance(collection_name, Unset):
        json_collection_name = UNSET
    else:
        json_collection_name = collection_name
    params["collection_name"] = json_collection_name

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/collections",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPaginatedResponseCollectionDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]:
    """Get Collections

     Get a list of collections for a logged-in user.

    This endpoint retrieves collections for a logged-in user in a paginated format.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[CollectionDTO]**: A paginated response containing collection information.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    collection_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]:
    """Get Collections

     Get a list of collections for a logged-in user.

    This endpoint retrieves collections for a logged-in user in a paginated format.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[CollectionDTO]**: A paginated response containing collection information.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]
    """

    return sync_detailed(
        client=client,
        collection_name=collection_name,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]:
    """Get Collections

     Get a list of collections for a logged-in user.

    This endpoint retrieves collections for a logged-in user in a paginated format.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[CollectionDTO]**: A paginated response containing collection information.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collection_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]]:
    """Get Collections

     Get a list of collections for a logged-in user.

    This endpoint retrieves collections for a logged-in user in a paginated format.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[CollectionDTO]**: A paginated response containing collection information.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseCollectionDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_name=collection_name,
            page=page,
            per_page=per_page,
        )
    ).parsed
