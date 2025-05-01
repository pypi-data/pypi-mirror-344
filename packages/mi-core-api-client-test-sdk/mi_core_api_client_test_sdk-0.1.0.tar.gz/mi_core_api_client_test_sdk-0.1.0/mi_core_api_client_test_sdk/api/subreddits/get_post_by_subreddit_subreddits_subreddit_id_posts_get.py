from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_reddit_post_schema_document import PaginatedResponseRedditPostSchemaDocument
from ...types import UNSET, Response, Unset


def _get_kwargs(
    subreddit_id: UUID,
    *,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/subreddits/{subreddit_id}/posts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseRedditPostSchemaDocument.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]:
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
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]:
    """Get Post By Subreddit

     Get paginated posts from a specific subreddit.

    This endpoint retrieves a paginated list of posts from a given subreddit based on its ID.

    Args:
    - **subreddit_id**: The ID of the subreddit to fetch posts from.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[RedditPostSchema]**: A paginated response containing Reddit posts.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]
    """

    kwargs = _get_kwargs(
        subreddit_id=subreddit_id,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]:
    """Get Post By Subreddit

     Get paginated posts from a specific subreddit.

    This endpoint retrieves a paginated list of posts from a given subreddit based on its ID.

    Args:
    - **subreddit_id**: The ID of the subreddit to fetch posts from.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[RedditPostSchema]**: A paginated response containing Reddit posts.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]
    """

    return sync_detailed(
        subreddit_id=subreddit_id,
        client=client,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]:
    """Get Post By Subreddit

     Get paginated posts from a specific subreddit.

    This endpoint retrieves a paginated list of posts from a given subreddit based on its ID.

    Args:
    - **subreddit_id**: The ID of the subreddit to fetch posts from.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[RedditPostSchema]**: A paginated response containing Reddit posts.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]
    """

    kwargs = _get_kwargs(
        subreddit_id=subreddit_id,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    subreddit_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]]:
    """Get Post By Subreddit

     Get paginated posts from a specific subreddit.

    This endpoint retrieves a paginated list of posts from a given subreddit based on its ID.

    Args:
    - **subreddit_id**: The ID of the subreddit to fetch posts from.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[RedditPostSchema]**: A paginated response containing Reddit posts.

    Raises:
    - **404 Not Found (RedditResultNotFoundException)**: Raised if no posts are found for the specified
    subreddit.

    Args:
        subreddit_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseRedditPostSchemaDocument]
    """

    return (
        await asyncio_detailed(
            subreddit_id=subreddit_id,
            client=client,
            page=page,
            per_page=per_page,
        )
    ).parsed
