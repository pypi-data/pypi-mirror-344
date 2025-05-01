from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_detailed_reddit_post_schema import (
    ResponseWithMetadataSchemaDetailedRedditPostSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    post_url: str,
    use_cache: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["post_url"] = post_url

    params["use_cache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/reddit/posts/details",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaDetailedRedditPostSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    post_url: str,
    use_cache: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]:
    """Get Post Details

     Retrieve detailed Reddit post information by URL.

    This endpoint retrieves detailed information about a specific Reddit post either from the database
    (cache)
    or directly from Reddit if it is not cached. The detailed information includes post data, author,
    and subreddit.

    Args:
    - **post_url**: The URL of the Reddit post to fetch details for.
    - **use_cache**: A boolean flag indicating whether to retrieve cached data from the database,
    default is True.

    Returns:
    - **DetailedRedditPostSchema**: A detailed representation of the Reddit post, including author and
    subreddit info.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        post_url (str):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]
    """

    kwargs = _get_kwargs(
        post_url=post_url,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    post_url: str,
    use_cache: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]:
    """Get Post Details

     Retrieve detailed Reddit post information by URL.

    This endpoint retrieves detailed information about a specific Reddit post either from the database
    (cache)
    or directly from Reddit if it is not cached. The detailed information includes post data, author,
    and subreddit.

    Args:
    - **post_url**: The URL of the Reddit post to fetch details for.
    - **use_cache**: A boolean flag indicating whether to retrieve cached data from the database,
    default is True.

    Returns:
    - **DetailedRedditPostSchema**: A detailed representation of the Reddit post, including author and
    subreddit info.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        post_url (str):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]
    """

    return sync_detailed(
        client=client,
        post_url=post_url,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    post_url: str,
    use_cache: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]:
    """Get Post Details

     Retrieve detailed Reddit post information by URL.

    This endpoint retrieves detailed information about a specific Reddit post either from the database
    (cache)
    or directly from Reddit if it is not cached. The detailed information includes post data, author,
    and subreddit.

    Args:
    - **post_url**: The URL of the Reddit post to fetch details for.
    - **use_cache**: A boolean flag indicating whether to retrieve cached data from the database,
    default is True.

    Returns:
    - **DetailedRedditPostSchema**: A detailed representation of the Reddit post, including author and
    subreddit info.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        post_url (str):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]
    """

    kwargs = _get_kwargs(
        post_url=post_url,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    post_url: str,
    use_cache: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]]:
    """Get Post Details

     Retrieve detailed Reddit post information by URL.

    This endpoint retrieves detailed information about a specific Reddit post either from the database
    (cache)
    or directly from Reddit if it is not cached. The detailed information includes post data, author,
    and subreddit.

    Args:
    - **post_url**: The URL of the Reddit post to fetch details for.
    - **use_cache**: A boolean flag indicating whether to retrieve cached data from the database,
    default is True.

    Returns:
    - **DetailedRedditPostSchema**: A detailed representation of the Reddit post, including author and
    subreddit info.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        post_url (str):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaDetailedRedditPostSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            post_url=post_url,
            use_cache=use_cache,
        )
    ).parsed
