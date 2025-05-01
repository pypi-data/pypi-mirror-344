import datetime
from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channel_average_values import ChannelAverageValues
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    channel_id: UUID,
    *,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.106932"),
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/channels/{channel_id}/avg-stats",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChannelAverageValues, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ChannelAverageValues.from_dict(response.json())

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
) -> Response[Union[ChannelAverageValues, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.106932"),
) -> Response[Union[ChannelAverageValues, HTTPValidationError]]:
    """Get Channel Avg Stats

     Get average statistics for a YouTube channel based on the provided time range.

    This endpoint returns the average statistics (views, likes, comments, etc.)
    for all videos from a specific YouTube channel within the given time range.

    Args:
    - **channel_id**: The unique ID of the channel.
    - **start_date**: The start date for calculating averages. Defaults to 1970-01-01.
    - **end_date**: The end date for calculating averages. Defaults to the current date.

    Returns:
    - **ChannelAverageValues**: An object containing the average statistics for the channel's videos.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: If no videos are found for the specified channel
    and time range.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.

    Args:
        channel_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.106932').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChannelAverageValues, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.106932"),
) -> Optional[Union[ChannelAverageValues, HTTPValidationError]]:
    """Get Channel Avg Stats

     Get average statistics for a YouTube channel based on the provided time range.

    This endpoint returns the average statistics (views, likes, comments, etc.)
    for all videos from a specific YouTube channel within the given time range.

    Args:
    - **channel_id**: The unique ID of the channel.
    - **start_date**: The start date for calculating averages. Defaults to 1970-01-01.
    - **end_date**: The end date for calculating averages. Defaults to the current date.

    Returns:
    - **ChannelAverageValues**: An object containing the average statistics for the channel's videos.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: If no videos are found for the specified channel
    and time range.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.

    Args:
        channel_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.106932').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChannelAverageValues, HTTPValidationError]
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.106932"),
) -> Response[Union[ChannelAverageValues, HTTPValidationError]]:
    """Get Channel Avg Stats

     Get average statistics for a YouTube channel based on the provided time range.

    This endpoint returns the average statistics (views, likes, comments, etc.)
    for all videos from a specific YouTube channel within the given time range.

    Args:
    - **channel_id**: The unique ID of the channel.
    - **start_date**: The start date for calculating averages. Defaults to 1970-01-01.
    - **end_date**: The end date for calculating averages. Defaults to the current date.

    Returns:
    - **ChannelAverageValues**: An object containing the average statistics for the channel's videos.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: If no videos are found for the specified channel
    and time range.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.

    Args:
        channel_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.106932').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChannelAverageValues, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.106932"),
) -> Optional[Union[ChannelAverageValues, HTTPValidationError]]:
    """Get Channel Avg Stats

     Get average statistics for a YouTube channel based on the provided time range.

    This endpoint returns the average statistics (views, likes, comments, etc.)
    for all videos from a specific YouTube channel within the given time range.

    Args:
    - **channel_id**: The unique ID of the channel.
    - **start_date**: The start date for calculating averages. Defaults to 1970-01-01.
    - **end_date**: The end date for calculating averages. Defaults to the current date.

    Returns:
    - **ChannelAverageValues**: An object containing the average statistics for the channel's videos.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: If no videos are found for the specified channel
    and time range.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.

    Args:
        channel_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.106932').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChannelAverageValues, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
