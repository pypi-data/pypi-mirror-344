import datetime
from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.subreddit_average_values import SubredditAverageValues
from ...types import UNSET, Response, Unset


def _get_kwargs(
    subreddit_id: UUID,
    *,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.124611"),
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
        "url": f"/subreddits/{subreddit_id}/avg-stats",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SubredditAverageValues]]:
    if response.status_code == 200:
        response_200 = SubredditAverageValues.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SubredditAverageValues]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.124611"),
) -> Response[Union[HTTPValidationError, SubredditAverageValues]]:
    """Get Channel Avg Stats

     Get average statistics for a subreddit within a date range.

    This endpoint retrieves the average statistics (such as average upvotes, comments, and word count)
    for a specific subreddit over the specified date range.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch statistics for.
    - **start_date**: The start date for calculating statistics, default is January 1, 1970.
    - **end_date**: The end date for calculating statistics, default is the current date.

    Returns:
    - **SubredditAverageValues**: The calculated average statistics for the subreddit, including
    upvotes, comments, and word count.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.

    Args:
        subreddit_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.124611').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SubredditAverageValues]]
    """

    kwargs = _get_kwargs(
        subreddit_id=subreddit_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.124611"),
) -> Optional[Union[HTTPValidationError, SubredditAverageValues]]:
    """Get Channel Avg Stats

     Get average statistics for a subreddit within a date range.

    This endpoint retrieves the average statistics (such as average upvotes, comments, and word count)
    for a specific subreddit over the specified date range.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch statistics for.
    - **start_date**: The start date for calculating statistics, default is January 1, 1970.
    - **end_date**: The end date for calculating statistics, default is the current date.

    Returns:
    - **SubredditAverageValues**: The calculated average statistics for the subreddit, including
    upvotes, comments, and word count.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.

    Args:
        subreddit_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.124611').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SubredditAverageValues]
    """

    return sync_detailed(
        subreddit_id=subreddit_id,
        client=client,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.124611"),
) -> Response[Union[HTTPValidationError, SubredditAverageValues]]:
    """Get Channel Avg Stats

     Get average statistics for a subreddit within a date range.

    This endpoint retrieves the average statistics (such as average upvotes, comments, and word count)
    for a specific subreddit over the specified date range.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch statistics for.
    - **start_date**: The start date for calculating statistics, default is January 1, 1970.
    - **end_date**: The end date for calculating statistics, default is the current date.

    Returns:
    - **SubredditAverageValues**: The calculated average statistics for the subreddit, including
    upvotes, comments, and word count.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.

    Args:
        subreddit_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.124611').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SubredditAverageValues]]
    """

    kwargs = _get_kwargs(
        subreddit_id=subreddit_id,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:14.124611"),
) -> Optional[Union[HTTPValidationError, SubredditAverageValues]]:
    """Get Channel Avg Stats

     Get average statistics for a subreddit within a date range.

    This endpoint retrieves the average statistics (such as average upvotes, comments, and word count)
    for a specific subreddit over the specified date range.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch statistics for.
    - **start_date**: The start date for calculating statistics, default is January 1, 1970.
    - **end_date**: The end date for calculating statistics, default is the current date.

    Returns:
    - **SubredditAverageValues**: The calculated average statistics for the subreddit, including
    upvotes, comments, and word count.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: If there is a database connection issue.

    Args:
        subreddit_id (UUID):
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:14.124611').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SubredditAverageValues]
    """

    return (
        await asyncio_detailed(
            subreddit_id=subreddit_id,
            client=client,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
