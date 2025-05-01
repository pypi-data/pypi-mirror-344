import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_reddit_post_schema_document_error_dto import (
    ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO,
)
from ...models.sort_options import SortOptions
from ...models.time_filter import TimeFilter
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    subreddit: str,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, SortOptions] = UNSET,
    time_filter: Union[Unset, TimeFilter] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["subreddit"] = subreddit

    json_total_posts: Union[None, Unset, int]
    if isinstance(total_posts, Unset):
        json_total_posts = UNSET
    else:
        json_total_posts = total_posts
    params["total_posts"] = json_total_posts

    params["max_duration_sec"] = max_duration_sec

    json_post_timestamp: Union[None, Unset, str]
    if isinstance(post_timestamp, Unset):
        json_post_timestamp = UNSET
    elif isinstance(post_timestamp, datetime.datetime):
        json_post_timestamp = post_timestamp.isoformat()
    else:
        json_post_timestamp = post_timestamp
    params["post_timestamp"] = json_post_timestamp

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sort_by"] = json_sort_by

    json_time_filter: Union[Unset, str] = UNSET
    if not isinstance(time_filter, Unset):
        json_time_filter = time_filter.value

    params["time_filter"] = json_time_filter

    params["use_cache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/reddit/subreddits/posts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    subreddit: str,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, SortOptions] = UNSET,
    time_filter: Union[Unset, TimeFilter] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]:
    """Collect Subreddit Posts

     Collect Reddit posts from a subreddit.

    This endpoint retrieves Reddit posts from a specified subreddit using a combination of optional
    filters
    and stop triggers. Posts can be collected from the database (cached) or directly from Reddit.

    Args:
    - **subreddit**: The name of the subreddit to retrieve posts from.
    - **total_posts**: The total number of posts to collect (optional).
    - **max_duration_sec**: The maximum time duration (in seconds) for collecting posts.
    - **post_timestamp**: A timestamp to filter posts created after this date.
    - **sort_by**: Sorting option for the posts (default is 'HOT').
    - **use_cache**: Whether to retrieve cached posts from the database (default is True).

    Returns:
    - **list[Union[RedditPostSchema, ErrorDTO]]**: A list of collected posts or errors.

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
        subreddit (str):
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter subreddit
            posts created after this date
        sort_by (Union[Unset, SortOptions]):
        time_filter (Union[Unset, TimeFilter]):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]
    """

    kwargs = _get_kwargs(
        subreddit=subreddit,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
        sort_by=sort_by,
        time_filter=time_filter,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    subreddit: str,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, SortOptions] = UNSET,
    time_filter: Union[Unset, TimeFilter] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]:
    """Collect Subreddit Posts

     Collect Reddit posts from a subreddit.

    This endpoint retrieves Reddit posts from a specified subreddit using a combination of optional
    filters
    and stop triggers. Posts can be collected from the database (cached) or directly from Reddit.

    Args:
    - **subreddit**: The name of the subreddit to retrieve posts from.
    - **total_posts**: The total number of posts to collect (optional).
    - **max_duration_sec**: The maximum time duration (in seconds) for collecting posts.
    - **post_timestamp**: A timestamp to filter posts created after this date.
    - **sort_by**: Sorting option for the posts (default is 'HOT').
    - **use_cache**: Whether to retrieve cached posts from the database (default is True).

    Returns:
    - **list[Union[RedditPostSchema, ErrorDTO]]**: A list of collected posts or errors.

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
        subreddit (str):
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter subreddit
            posts created after this date
        sort_by (Union[Unset, SortOptions]):
        time_filter (Union[Unset, TimeFilter]):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]
    """

    return sync_detailed(
        client=client,
        subreddit=subreddit,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
        sort_by=sort_by,
        time_filter=time_filter,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    subreddit: str,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, SortOptions] = UNSET,
    time_filter: Union[Unset, TimeFilter] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]:
    """Collect Subreddit Posts

     Collect Reddit posts from a subreddit.

    This endpoint retrieves Reddit posts from a specified subreddit using a combination of optional
    filters
    and stop triggers. Posts can be collected from the database (cached) or directly from Reddit.

    Args:
    - **subreddit**: The name of the subreddit to retrieve posts from.
    - **total_posts**: The total number of posts to collect (optional).
    - **max_duration_sec**: The maximum time duration (in seconds) for collecting posts.
    - **post_timestamp**: A timestamp to filter posts created after this date.
    - **sort_by**: Sorting option for the posts (default is 'HOT').
    - **use_cache**: Whether to retrieve cached posts from the database (default is True).

    Returns:
    - **list[Union[RedditPostSchema, ErrorDTO]]**: A list of collected posts or errors.

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
        subreddit (str):
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter subreddit
            posts created after this date
        sort_by (Union[Unset, SortOptions]):
        time_filter (Union[Unset, TimeFilter]):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]
    """

    kwargs = _get_kwargs(
        subreddit=subreddit,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
        sort_by=sort_by,
        time_filter=time_filter,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    subreddit: str,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    sort_by: Union[Unset, SortOptions] = UNSET,
    time_filter: Union[Unset, TimeFilter] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]]:
    """Collect Subreddit Posts

     Collect Reddit posts from a subreddit.

    This endpoint retrieves Reddit posts from a specified subreddit using a combination of optional
    filters
    and stop triggers. Posts can be collected from the database (cached) or directly from Reddit.

    Args:
    - **subreddit**: The name of the subreddit to retrieve posts from.
    - **total_posts**: The total number of posts to collect (optional).
    - **max_duration_sec**: The maximum time duration (in seconds) for collecting posts.
    - **post_timestamp**: A timestamp to filter posts created after this date.
    - **sort_by**: Sorting option for the posts (default is 'HOT').
    - **use_cache**: Whether to retrieve cached posts from the database (default is True).

    Returns:
    - **list[Union[RedditPostSchema, ErrorDTO]]**: A list of collected posts or errors.

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
        subreddit (str):
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter subreddit
            posts created after this date
        sort_by (Union[Unset, SortOptions]):
        time_filter (Union[Unset, TimeFilter]):
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionRedditPostSchemaDocumentErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            subreddit=subreddit,
            total_posts=total_posts,
            max_duration_sec=max_duration_sec,
            post_timestamp=post_timestamp,
            sort_by=sort_by,
            time_filter=time_filter,
            use_cache=use_cache,
        )
    ).parsed
