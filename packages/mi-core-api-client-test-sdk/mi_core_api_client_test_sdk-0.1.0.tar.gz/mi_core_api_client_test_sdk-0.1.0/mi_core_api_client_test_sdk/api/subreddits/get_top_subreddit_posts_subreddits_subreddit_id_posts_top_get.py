from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.reddit_post_schema_document import RedditPostSchemaDocument
from ...types import Response


def _get_kwargs(
    subreddit_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/subreddits/{subreddit_id}/posts/top",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, RedditPostSchemaDocument]]:
    if response.status_code == 200:
        response_200 = RedditPostSchemaDocument.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, RedditPostSchemaDocument]]:
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
) -> Response[Union[HTTPValidationError, RedditPostSchemaDocument]]:
    """Get Top Subreddit Posts

     Get the top post from a specific subreddit.

    This endpoint retrieves the most popular (top) post from the given subreddit by its ID.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch the top post from.

    Returns:
    - **RedditPostSchema**: The top post of the specified subreddit.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RedditPostSchemaDocument]]
    """

    kwargs = _get_kwargs(
        subreddit_id=subreddit_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, RedditPostSchemaDocument]]:
    """Get Top Subreddit Posts

     Get the top post from a specific subreddit.

    This endpoint retrieves the most popular (top) post from the given subreddit by its ID.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch the top post from.

    Returns:
    - **RedditPostSchema**: The top post of the specified subreddit.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RedditPostSchemaDocument]
    """

    return sync_detailed(
        subreddit_id=subreddit_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, RedditPostSchemaDocument]]:
    """Get Top Subreddit Posts

     Get the top post from a specific subreddit.

    This endpoint retrieves the most popular (top) post from the given subreddit by its ID.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch the top post from.

    Returns:
    - **RedditPostSchema**: The top post of the specified subreddit.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RedditPostSchemaDocument]]
    """

    kwargs = _get_kwargs(
        subreddit_id=subreddit_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, RedditPostSchemaDocument]]:
    """Get Top Subreddit Posts

     Get the top post from a specific subreddit.

    This endpoint retrieves the most popular (top) post from the given subreddit by its ID.

    Args:
    - **subreddit_id**: The UUID of the subreddit to fetch the top post from.

    Returns:
    - **RedditPostSchema**: The top post of the specified subreddit.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RedditPostSchemaDocument]
    """

    return (
        await asyncio_detailed(
            subreddit_id=subreddit_id,
            client=client,
        )
    ).parsed
