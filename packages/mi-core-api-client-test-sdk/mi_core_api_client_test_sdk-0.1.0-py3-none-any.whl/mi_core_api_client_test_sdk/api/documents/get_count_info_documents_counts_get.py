from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document_count_info import DocumentCountInfo
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/documents/counts",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DocumentCountInfo]:
    if response.status_code == 200:
        response_200 = DocumentCountInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DocumentCountInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DocumentCountInfo]:
    """Get Count Info

     Get the total count of all documents.

    This endpoint returns an object containing counts for various document types like YouTube channels,
    subreddits, etc.

    Returns:
    - **DocumentCountInfo**: An object of DocumentCountInfo containing document counts for various
    types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentCountInfo]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DocumentCountInfo]:
    """Get Count Info

     Get the total count of all documents.

    This endpoint returns an object containing counts for various document types like YouTube channels,
    subreddits, etc.

    Returns:
    - **DocumentCountInfo**: An object of DocumentCountInfo containing document counts for various
    types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentCountInfo
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DocumentCountInfo]:
    """Get Count Info

     Get the total count of all documents.

    This endpoint returns an object containing counts for various document types like YouTube channels,
    subreddits, etc.

    Returns:
    - **DocumentCountInfo**: An object of DocumentCountInfo containing document counts for various
    types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentCountInfo]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DocumentCountInfo]:
    """Get Count Info

     Get the total count of all documents.

    This endpoint returns an object containing counts for various document types like YouTube channels,
    subreddits, etc.

    Returns:
    - **DocumentCountInfo**: An object of DocumentCountInfo containing document counts for various
    types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentCountInfo
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
