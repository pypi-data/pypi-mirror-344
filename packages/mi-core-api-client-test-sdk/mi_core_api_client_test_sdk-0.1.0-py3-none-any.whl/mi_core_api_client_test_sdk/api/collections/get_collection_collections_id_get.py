from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_union_collection_with_sources_dto_collection import (
    ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    with_sources: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["with_sources"] = with_sources

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/collections/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
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
    with_sources: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection

     Get a detailed collection by ID.

    Retrieves collection and its attached sources by the provided ID.

    Args:
    - **id**: The UUID of the collection to fetch.
    Returns:
    - **CollectionWithSourcesDTO**: A schema containing information about the collection and its
    sources.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if the collection with the provided ID is not found.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]
    """

    kwargs = _get_kwargs(
        id=id,
        with_sources=with_sources,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection

     Get a detailed collection by ID.

    Retrieves collection and its attached sources by the provided ID.

    Args:
    - **id**: The UUID of the collection to fetch.
    Returns:
    - **CollectionWithSourcesDTO**: A schema containing information about the collection and its
    sources.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if the collection with the provided ID is not found.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]
    """

    return sync_detailed(
        id=id,
        client=client,
        with_sources=with_sources,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection

     Get a detailed collection by ID.

    Retrieves collection and its attached sources by the provided ID.

    Args:
    - **id**: The UUID of the collection to fetch.
    Returns:
    - **CollectionWithSourcesDTO**: A schema containing information about the collection and its
    sources.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if the collection with the provided ID is not found.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]
    """

    kwargs = _get_kwargs(
        id=id,
        with_sources=with_sources,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection

     Get a detailed collection by ID.

    Retrieves collection and its attached sources by the provided ID.

    Args:
    - **id**: The UUID of the collection to fetch.
    Returns:
    - **CollectionWithSourcesDTO**: A schema containing information about the collection and its
    sources.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if the collection with the provided ID is not found.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            with_sources=with_sources,
        )
    ).parsed
