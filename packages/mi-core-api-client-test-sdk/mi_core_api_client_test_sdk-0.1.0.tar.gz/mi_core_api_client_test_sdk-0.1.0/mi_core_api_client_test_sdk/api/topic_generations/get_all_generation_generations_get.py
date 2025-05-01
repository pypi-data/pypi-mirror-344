from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_paginated_response_generation_schema import (
    ResponseWithMetadataSchemaPaginatedResponseGenerationSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    topic: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_topic: Union[None, Unset, str]
    if isinstance(topic, Unset):
        json_topic = UNSET
    else:
        json_topic = topic
    params["topic"] = json_topic

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/generations",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPaginatedResponseGenerationSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    topic: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]:
    """Get All Generation

     Get all generation with topic name. Allowed only for admin or moder

    Args:
        topic (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]
    """

    kwargs = _get_kwargs(
        topic=topic,
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
    topic: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]:
    """Get All Generation

     Get all generation with topic name. Allowed only for admin or moder

    Args:
        topic (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]
    """

    return sync_detailed(
        client=client,
        topic=topic,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    topic: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]:
    """Get All Generation

     Get all generation with topic name. Allowed only for admin or moder

    Args:
        topic (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]
    """

    kwargs = _get_kwargs(
        topic=topic,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    topic: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]]:
    """Get All Generation

     Get all generation with topic name. Allowed only for admin or moder

    Args:
        topic (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseGenerationSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            topic=topic,
            page=page,
            per_page=per_page,
        )
    ).parsed
