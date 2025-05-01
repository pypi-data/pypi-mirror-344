from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_union_collection_with_sources_dto_collection import (
    ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    with_sources: Union[Unset, bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["with_sources"] = with_sources

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/collections/{name}/",
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
    name: str,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = False,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection By Name

    Args:
        name (str):
        with_sources (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]
    """

    kwargs = _get_kwargs(
        name=name,
        with_sources=with_sources,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = False,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection By Name

    Args:
        name (str):
        with_sources (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]
    """

    return sync_detailed(
        name=name,
        client=client,
        with_sources=with_sources,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = False,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection By Name

    Args:
        name (str):
        with_sources (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]
    """

    kwargs = _get_kwargs(
        name=name,
        with_sources=with_sources,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = False,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]]:
    """Get Collection By Name

    Args:
        name (str):
        with_sources (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUnionCollectionWithSourcesDTOCollection]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            with_sources=with_sources,
        )
    ).parsed
