from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_collection_status_response import (
    ResponseWithMetadataSchemaCollectionStatusResponse,
)
from ...types import Response


def _get_kwargs(
    id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/collections/{id}/status",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaCollectionStatusResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]:
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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]:
    """Get Collections Status

     Get status of all sources in a collection.

    This endpoint returns statistics about sources in the collection:
    - collection_status: General collection status obtained from sources statuses information
    - total_number: Total number of sources in the collection
    - collected_number: Number of sources that have been collected
    - created: Number of sources in 'created' status
    - processing: Number of sources currently being processed
    - completed: Number of sources that finished processing successfully
    - failed: Number of sources that failed processing

    Args:
    - **id**: The UUID of the collection to check status for

    Returns:
    - **CollectionStatusResponse**: A schema containing status information about the collection's
    sources.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]
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
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]:
    """Get Collections Status

     Get status of all sources in a collection.

    This endpoint returns statistics about sources in the collection:
    - collection_status: General collection status obtained from sources statuses information
    - total_number: Total number of sources in the collection
    - collected_number: Number of sources that have been collected
    - created: Number of sources in 'created' status
    - processing: Number of sources currently being processed
    - completed: Number of sources that finished processing successfully
    - failed: Number of sources that failed processing

    Args:
    - **id**: The UUID of the collection to check status for

    Returns:
    - **CollectionStatusResponse**: A schema containing status information about the collection's
    sources.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]:
    """Get Collections Status

     Get status of all sources in a collection.

    This endpoint returns statistics about sources in the collection:
    - collection_status: General collection status obtained from sources statuses information
    - total_number: Total number of sources in the collection
    - collected_number: Number of sources that have been collected
    - created: Number of sources in 'created' status
    - processing: Number of sources currently being processed
    - completed: Number of sources that finished processing successfully
    - failed: Number of sources that failed processing

    Args:
    - **id**: The UUID of the collection to check status for

    Returns:
    - **CollectionStatusResponse**: A schema containing status information about the collection's
    sources.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]
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
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]]:
    """Get Collections Status

     Get status of all sources in a collection.

    This endpoint returns statistics about sources in the collection:
    - collection_status: General collection status obtained from sources statuses information
    - total_number: Total number of sources in the collection
    - collected_number: Number of sources that have been collected
    - created: Number of sources in 'created' status
    - processing: Number of sources currently being processed
    - completed: Number of sources that finished processing successfully
    - failed: Number of sources that failed processing

    Args:
    - **id**: The UUID of the collection to check status for

    Returns:
    - **CollectionStatusResponse**: A schema containing status information about the collection's
    sources.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionStatusResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
