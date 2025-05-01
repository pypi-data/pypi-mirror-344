from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_reddit_post_schema_document_reddit_post_with_comments_schema_error_dto import (
    ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    queries: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    total_posts: Union[Unset, int] = 5,
    with_comments: Union[Unset, bool] = True,
    use_cache: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_queries = queries

    params["queries"] = json_queries

    params["max_duration_sec"] = max_duration_sec

    params["total_posts"] = total_posts

    params["with_comments"] = with_comments

    params["use_cache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/reddit/posts/comments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
    ]
]:
    if response.status_code == 200:
        response_200 = (
            ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO.from_dict(
                response.json()
            )
        )

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
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    total_posts: Union[Unset, int] = 5,
    with_comments: Union[Unset, bool] = True,
    use_cache: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
    ]
]:
    """Get Post And Comments

     Retrieve Reddit posts and optionally their comments by search queries.

    This endpoint retrieves Reddit posts and optionally their comments based on the provided search
    queries.
    The retrieval process can use cached data if available, or fetch the data directly from Reddit.
    Results are limited by the specified maximum duration and total number of posts.

    Args:
    - **queries**: List of search queries to fetch Reddit posts and comments for.
    - **max_duration_sec**: Maximum duration in seconds to fetch the posts, default is 60.
    - **total_posts**: Total number of posts to fetch, default is 5.
    - **with_comments**: Boolean indicating whether to include comments in the results, default is True.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[RedditPostSchema, RedditPostWithCommentsSchema, ErrorDTO]]**:
        A list of Reddit posts, optionally including their comments, or errors if encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction failed for all
    URLs.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        queries (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        total_posts (Union[Unset, int]):  Default: 5.
        with_comments (Union[Unset, bool]):  Default: True.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        max_duration_sec=max_duration_sec,
        total_posts=total_posts,
        with_comments=with_comments,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    total_posts: Union[Unset, int] = 5,
    with_comments: Union[Unset, bool] = True,
    use_cache: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
    ]
]:
    """Get Post And Comments

     Retrieve Reddit posts and optionally their comments by search queries.

    This endpoint retrieves Reddit posts and optionally their comments based on the provided search
    queries.
    The retrieval process can use cached data if available, or fetch the data directly from Reddit.
    Results are limited by the specified maximum duration and total number of posts.

    Args:
    - **queries**: List of search queries to fetch Reddit posts and comments for.
    - **max_duration_sec**: Maximum duration in seconds to fetch the posts, default is 60.
    - **total_posts**: Total number of posts to fetch, default is 5.
    - **with_comments**: Boolean indicating whether to include comments in the results, default is True.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[RedditPostSchema, RedditPostWithCommentsSchema, ErrorDTO]]**:
        A list of Reddit posts, optionally including their comments, or errors if encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction failed for all
    URLs.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        queries (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        total_posts (Union[Unset, int]):  Default: 5.
        with_comments (Union[Unset, bool]):  Default: True.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO]
    """

    return sync_detailed(
        client=client,
        queries=queries,
        max_duration_sec=max_duration_sec,
        total_posts=total_posts,
        with_comments=with_comments,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    total_posts: Union[Unset, int] = 5,
    with_comments: Union[Unset, bool] = True,
    use_cache: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
    ]
]:
    """Get Post And Comments

     Retrieve Reddit posts and optionally their comments by search queries.

    This endpoint retrieves Reddit posts and optionally their comments based on the provided search
    queries.
    The retrieval process can use cached data if available, or fetch the data directly from Reddit.
    Results are limited by the specified maximum duration and total number of posts.

    Args:
    - **queries**: List of search queries to fetch Reddit posts and comments for.
    - **max_duration_sec**: Maximum duration in seconds to fetch the posts, default is 60.
    - **total_posts**: Total number of posts to fetch, default is 5.
    - **with_comments**: Boolean indicating whether to include comments in the results, default is True.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[RedditPostSchema, RedditPostWithCommentsSchema, ErrorDTO]]**:
        A list of Reddit posts, optionally including their comments, or errors if encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction failed for all
    URLs.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        queries (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        total_posts (Union[Unset, int]):  Default: 5.
        with_comments (Union[Unset, bool]):  Default: True.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        max_duration_sec=max_duration_sec,
        total_posts=total_posts,
        with_comments=with_comments,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    total_posts: Union[Unset, int] = 5,
    with_comments: Union[Unset, bool] = True,
    use_cache: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO,
    ]
]:
    """Get Post And Comments

     Retrieve Reddit posts and optionally their comments by search queries.

    This endpoint retrieves Reddit posts and optionally their comments based on the provided search
    queries.
    The retrieval process can use cached data if available, or fetch the data directly from Reddit.
    Results are limited by the specified maximum duration and total number of posts.

    Args:
    - **queries**: List of search queries to fetch Reddit posts and comments for.
    - **max_duration_sec**: Maximum duration in seconds to fetch the posts, default is 60.
    - **total_posts**: Total number of posts to fetch, default is 5.
    - **with_comments**: Boolean indicating whether to include comments in the results, default is True.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[RedditPostSchema, RedditPostWithCommentsSchema, ErrorDTO]]**:
        A list of Reddit posts, optionally including their comments, or errors if encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (RedditResultNotFoundException)**: Raised if any of the specified URLs could not
    be found on Reddit.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction failed for all
    URLs.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if the API extraction method fails
    while fetching posts.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if the HTML extraction method fails
    while fetching posts.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        queries (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        total_posts (Union[Unset, int]):  Default: 5.
        with_comments (Union[Unset, bool]):  Default: True.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentRedditPostWithCommentsSchemaErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            queries=queries,
            max_duration_sec=max_duration_sec,
            total_posts=total_posts,
            with_comments=with_comments,
            use_cache=use_cache,
        )
    ).parsed
