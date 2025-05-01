from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.source_collect_type import SourceCollectType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collect_type: Union[Unset, SourceCollectType] = UNSET,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_collect_type: Union[Unset, str] = UNSET
    if not isinstance(collect_type, Unset):
        json_collect_type = collect_type.value

    params["collect_type"] = json_collect_type

    json_collection_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(collection_ids, Unset):
        json_collection_ids = []
        for collection_ids_item_data in collection_ids:
            collection_ids_item = str(collection_ids_item_data)
            json_collection_ids.append(collection_ids_item)

    params["collection_ids"] = json_collection_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/collections/collect",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    collect_type: Union[Unset, SourceCollectType] = UNSET,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Collections Collect

     Collect all data for sources from provided collections.

    This endpoint initiates collection of data for all sources from provided collections:
    - For channels, it will collect both channel info and videos
    - For subreddits, it will collect both subreddit info and posts
    - For articles, videos, and reddit posts, it will collect the content and metadata

    Args:
        collect_type (Union[Unset, SourceCollectType]): Enumeration class representing source
            collect types.
        collection_ids (Union[Unset, list[UUID]]): List of collection IDs to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collect_type=collect_type,
        collection_ids=collection_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    collect_type: Union[Unset, SourceCollectType] = UNSET,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Collections Collect

     Collect all data for sources from provided collections.

    This endpoint initiates collection of data for all sources from provided collections:
    - For channels, it will collect both channel info and videos
    - For subreddits, it will collect both subreddit info and posts
    - For articles, videos, and reddit posts, it will collect the content and metadata

    Args:
        collect_type (Union[Unset, SourceCollectType]): Enumeration class representing source
            collect types.
        collection_ids (Union[Unset, list[UUID]]): List of collection IDs to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        collect_type=collect_type,
        collection_ids=collection_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collect_type: Union[Unset, SourceCollectType] = UNSET,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Collections Collect

     Collect all data for sources from provided collections.

    This endpoint initiates collection of data for all sources from provided collections:
    - For channels, it will collect both channel info and videos
    - For subreddits, it will collect both subreddit info and posts
    - For articles, videos, and reddit posts, it will collect the content and metadata

    Args:
        collect_type (Union[Unset, SourceCollectType]): Enumeration class representing source
            collect types.
        collection_ids (Union[Unset, list[UUID]]): List of collection IDs to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collect_type=collect_type,
        collection_ids=collection_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collect_type: Union[Unset, SourceCollectType] = UNSET,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Collections Collect

     Collect all data for sources from provided collections.

    This endpoint initiates collection of data for all sources from provided collections:
    - For channels, it will collect both channel info and videos
    - For subreddits, it will collect both subreddit info and posts
    - For articles, videos, and reddit posts, it will collect the content and metadata

    Args:
        collect_type (Union[Unset, SourceCollectType]): Enumeration class representing source
            collect types.
        collection_ids (Union[Unset, list[UUID]]): List of collection IDs to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            collect_type=collect_type,
            collection_ids=collection_ids,
        )
    ).parsed
