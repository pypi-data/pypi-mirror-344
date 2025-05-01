from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.subreddit_info_schema import SubredditInfoSchema
from ...types import UNSET, Response


def _get_kwargs(
    *,
    subreddit_handle: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["subreddit_handle"] = subreddit_handle

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/subreddits/handle",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SubredditInfoSchema]]:
    if response.status_code == 200:
        response_200 = SubredditInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SubredditInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    subreddit_handle: str,
) -> Response[Union[HTTPValidationError, SubredditInfoSchema]]:
    """Get Subreddit Info By Name

     Get subreddit information by subreddit name.

    This endpoint returns detailed information about a subreddit based on the provided subreddit name.

    Args:
    - **subreddit_handle**: The name of the subreddit to retrieve. Can be a full URL, 'r/' prefixed, or
    just the subreddit name.

    Returns:
    - **SubredditInfoSchema**: Subreddit information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        subreddit_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SubredditInfoSchema]]
    """

    kwargs = _get_kwargs(
        subreddit_handle=subreddit_handle,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    subreddit_handle: str,
) -> Optional[Union[HTTPValidationError, SubredditInfoSchema]]:
    """Get Subreddit Info By Name

     Get subreddit information by subreddit name.

    This endpoint returns detailed information about a subreddit based on the provided subreddit name.

    Args:
    - **subreddit_handle**: The name of the subreddit to retrieve. Can be a full URL, 'r/' prefixed, or
    just the subreddit name.

    Returns:
    - **SubredditInfoSchema**: Subreddit information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        subreddit_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SubredditInfoSchema]
    """

    return sync_detailed(
        client=client,
        subreddit_handle=subreddit_handle,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    subreddit_handle: str,
) -> Response[Union[HTTPValidationError, SubredditInfoSchema]]:
    """Get Subreddit Info By Name

     Get subreddit information by subreddit name.

    This endpoint returns detailed information about a subreddit based on the provided subreddit name.

    Args:
    - **subreddit_handle**: The name of the subreddit to retrieve. Can be a full URL, 'r/' prefixed, or
    just the subreddit name.

    Returns:
    - **SubredditInfoSchema**: Subreddit information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        subreddit_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SubredditInfoSchema]]
    """

    kwargs = _get_kwargs(
        subreddit_handle=subreddit_handle,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    subreddit_handle: str,
) -> Optional[Union[HTTPValidationError, SubredditInfoSchema]]:
    """Get Subreddit Info By Name

     Get subreddit information by subreddit name.

    This endpoint returns detailed information about a subreddit based on the provided subreddit name.

    Args:
    - **subreddit_handle**: The name of the subreddit to retrieve. Can be a full URL, 'r/' prefixed, or
    just the subreddit name.

    Returns:
    - **SubredditInfoSchema**: Subreddit information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if the channel name is not found in the database.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        subreddit_handle (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SubredditInfoSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            subreddit_handle=subreddit_handle,
        )
    ).parsed
