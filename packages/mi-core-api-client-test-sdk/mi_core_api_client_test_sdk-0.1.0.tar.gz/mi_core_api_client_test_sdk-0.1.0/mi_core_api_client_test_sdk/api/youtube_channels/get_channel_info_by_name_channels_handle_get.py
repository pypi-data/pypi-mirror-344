from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.youtube_channel_info_schema import YoutubeChannelInfoSchema
from ...types import UNSET, Response


def _get_kwargs(
    *,
    channel_handle: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["channel_handle"] = channel_handle

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/channels/handle",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, YoutubeChannelInfoSchema]]:
    if response.status_code == 200:
        response_200 = YoutubeChannelInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, YoutubeChannelInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    channel_handle: str,
) -> Response[Union[HTTPValidationError, YoutubeChannelInfoSchema]]:
    """Get Channel Info By Name

     Get YouTube channel information by channel name.

    This endpoint returns detailed information about a YouTube channel based on the provided channel
    name.

    Args:
    - **channel_handle**: The name of the YouTube channel to retrieve. It can be with or without the '@'
    symbol.

    Returns:
    - **YoutubeChannelInfoSchema**: YouTube channel information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, YoutubeChannelInfoSchema]]
    """

    kwargs = _get_kwargs(
        channel_handle=channel_handle,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    channel_handle: str,
) -> Optional[Union[HTTPValidationError, YoutubeChannelInfoSchema]]:
    """Get Channel Info By Name

     Get YouTube channel information by channel name.

    This endpoint returns detailed information about a YouTube channel based on the provided channel
    name.

    Args:
    - **channel_handle**: The name of the YouTube channel to retrieve. It can be with or without the '@'
    symbol.

    Returns:
    - **YoutubeChannelInfoSchema**: YouTube channel information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, YoutubeChannelInfoSchema]
    """

    return sync_detailed(
        client=client,
        channel_handle=channel_handle,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    channel_handle: str,
) -> Response[Union[HTTPValidationError, YoutubeChannelInfoSchema]]:
    """Get Channel Info By Name

     Get YouTube channel information by channel name.

    This endpoint returns detailed information about a YouTube channel based on the provided channel
    name.

    Args:
    - **channel_handle**: The name of the YouTube channel to retrieve. It can be with or without the '@'
    symbol.

    Returns:
    - **YoutubeChannelInfoSchema**: YouTube channel information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, YoutubeChannelInfoSchema]]
    """

    kwargs = _get_kwargs(
        channel_handle=channel_handle,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    channel_handle: str,
) -> Optional[Union[HTTPValidationError, YoutubeChannelInfoSchema]]:
    """Get Channel Info By Name

     Get YouTube channel information by channel name.

    This endpoint returns detailed information about a YouTube channel based on the provided channel
    name.

    Args:
    - **channel_handle**: The name of the YouTube channel to retrieve. It can be with or without the '@'
    symbol.

    Returns:
    - **YoutubeChannelInfoSchema**: YouTube channel information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, YoutubeChannelInfoSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            channel_handle=channel_handle,
        )
    ).parsed
