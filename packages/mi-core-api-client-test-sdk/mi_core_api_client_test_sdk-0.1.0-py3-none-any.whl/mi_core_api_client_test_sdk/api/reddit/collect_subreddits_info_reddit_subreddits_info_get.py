from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_subreddit_info_schema_subreddit_info_with_posts_schema_error_dto import (
    ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    subreddits: list[str],
    use_cache: Union[Unset, bool] = True,
    with_last_posts_info: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_subreddits = subreddits

    params["subreddits"] = json_subreddits

    params["use_cache"] = use_cache

    params["with_last_posts_info"] = with_last_posts_info

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/reddit/subreddits/info",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO
    ]
]:
    if response.status_code == 200:
        response_200 = (
            ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO.from_dict(
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
        HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO
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
    subreddits: list[str],
    use_cache: Union[Unset, bool] = True,
    with_last_posts_info: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO
    ]
]:
    """Collect Subreddits Info

     Collect subreddit information with optional last post details.

    This endpoint retrieves information for multiple subreddits and optionally includes details
    about the last posts in each subreddit. It can use cached data or fetch fresh data from Reddit.

    Args:
    - **subreddits**: A list of subreddit names to retrieve information for.
    - **use_cache**: Whether to use cached data (default is True).
    - **with_last_posts_info**: Whether to include the latest post information in the response (default
    is True).

    Returns:
    - **list[Union[SubredditInfoSchema, SubredditInfoWithPostsSchema, ErrorDTO]**:
        A list of subreddit information or errors.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (ZyteAPIQuotaExceeded)**: Raised if the API quota for the external service is
    exceeded.
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
        subreddits (list[str]):
        use_cache (Union[Unset, bool]):  Default: True.
        with_last_posts_info (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        subreddits=subreddits,
        use_cache=use_cache,
        with_last_posts_info=with_last_posts_info,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    subreddits: list[str],
    use_cache: Union[Unset, bool] = True,
    with_last_posts_info: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO
    ]
]:
    """Collect Subreddits Info

     Collect subreddit information with optional last post details.

    This endpoint retrieves information for multiple subreddits and optionally includes details
    about the last posts in each subreddit. It can use cached data or fetch fresh data from Reddit.

    Args:
    - **subreddits**: A list of subreddit names to retrieve information for.
    - **use_cache**: Whether to use cached data (default is True).
    - **with_last_posts_info**: Whether to include the latest post information in the response (default
    is True).

    Returns:
    - **list[Union[SubredditInfoSchema, SubredditInfoWithPostsSchema, ErrorDTO]**:
        A list of subreddit information or errors.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (ZyteAPIQuotaExceeded)**: Raised if the API quota for the external service is
    exceeded.
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
        subreddits (list[str]):
        use_cache (Union[Unset, bool]):  Default: True.
        with_last_posts_info (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO]
    """

    return sync_detailed(
        client=client,
        subreddits=subreddits,
        use_cache=use_cache,
        with_last_posts_info=with_last_posts_info,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    subreddits: list[str],
    use_cache: Union[Unset, bool] = True,
    with_last_posts_info: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO
    ]
]:
    """Collect Subreddits Info

     Collect subreddit information with optional last post details.

    This endpoint retrieves information for multiple subreddits and optionally includes details
    about the last posts in each subreddit. It can use cached data or fetch fresh data from Reddit.

    Args:
    - **subreddits**: A list of subreddit names to retrieve information for.
    - **use_cache**: Whether to use cached data (default is True).
    - **with_last_posts_info**: Whether to include the latest post information in the response (default
    is True).

    Returns:
    - **list[Union[SubredditInfoSchema, SubredditInfoWithPostsSchema, ErrorDTO]**:
        A list of subreddit information or errors.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (ZyteAPIQuotaExceeded)**: Raised if the API quota for the external service is
    exceeded.
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
        subreddits (list[str]):
        use_cache (Union[Unset, bool]):  Default: True.
        with_last_posts_info (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        subreddits=subreddits,
        use_cache=use_cache,
        with_last_posts_info=with_last_posts_info,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    subreddits: list[str],
    use_cache: Union[Unset, bool] = True,
    with_last_posts_info: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO
    ]
]:
    """Collect Subreddits Info

     Collect subreddit information with optional last post details.

    This endpoint retrieves information for multiple subreddits and optionally includes details
    about the last posts in each subreddit. It can use cached data or fetch fresh data from Reddit.

    Args:
    - **subreddits**: A list of subreddit names to retrieve information for.
    - **use_cache**: Whether to use cached data (default is True).
    - **with_last_posts_info**: Whether to include the latest post information in the response (default
    is True).

    Returns:
    - **list[Union[SubredditInfoSchema, SubredditInfoWithPostsSchema, ErrorDTO]**:
        A list of subreddit information or errors.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (ZyteAPIQuotaExceeded)**: Raised if the API quota for the external service is
    exceeded.
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
        subreddits (list[str]):
        use_cache (Union[Unset, bool]):  Default: True.
        with_last_posts_info (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionSubredditInfoSchemaSubredditInfoWithPostsSchemaErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            subreddits=subreddits,
            use_cache=use_cache,
            with_last_posts_info=with_last_posts_info,
        )
    ).parsed
