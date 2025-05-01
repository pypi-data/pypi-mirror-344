from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_source_status_response import (
    ResponseWithMetadataSchemalistSourceStatusResponse,
)
from ...types import UNSET, Response


def _get_kwargs(
    *,
    source_ids: list[UUID],
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_source_ids = []
    for source_ids_item_data in source_ids:
        source_ids_item = str(source_ids_item_data)
        json_source_ids.append(source_ids_item)

    params["source_ids"] = json_source_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sources/status",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistSourceStatusResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    source_ids: list[UUID],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]:
    """Get Sources Status

    Args:
        source_ids (list[UUID]): List of source IDs to check status for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]
    """

    kwargs = _get_kwargs(
        source_ids=source_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    source_ids: list[UUID],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]:
    """Get Sources Status

    Args:
        source_ids (list[UUID]): List of source IDs to check status for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]
    """

    return sync_detailed(
        client=client,
        source_ids=source_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    source_ids: list[UUID],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]:
    """Get Sources Status

    Args:
        source_ids (list[UUID]): List of source IDs to check status for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]
    """

    kwargs = _get_kwargs(
        source_ids=source_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    source_ids: list[UUID],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]]:
    """Get Sources Status

    Args:
        source_ids (list[UUID]): List of source IDs to check status for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceStatusResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            source_ids=source_ids,
        )
    ).parsed
