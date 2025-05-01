from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_youtube_video_with_comments_dto_youtube_video_with_comments_and_transcript_schema_error_dto import (
    ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
)
from ...models.serp_search_engine import SerpSearchEngine
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    channel: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["channel"] = channel

    params["with_transcript"] = with_transcript

    params["total_posts"] = total_posts

    params["max_duration_sec"] = max_duration_sec

    params["use_cache"] = use_cache

    json_engine: Union[Unset, str] = UNSET
    if not isinstance(engine, Unset):
        json_engine = engine.value

    params["engine"] = json_engine

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/youtube/videos/comments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
    ]
]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO.from_dict(
            response.json()
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
        ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
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
    channel: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
    ]
]:
    """Get Video And Comments By Query

     Retrieves YouTube videos and their comments based on a channel search query.

    This endpoint fetches YouTube videos and their associated comments for a specific channel
    based on the query provided. It uses stop triggers to control the number of posts retrieved
    and the maximum duration for the process. Caching is available to reduce redundant requests.

    Args:
    - **channel**: The channel name to query YouTube videos from, example is 'Formula1'.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of posts to retrieve, default is 5.
    - **max_duration_sec**: The maximum duration for retrieving data in seconds, default is 60.
    - **use_cache**: Boolean flag indicating whether to use cached data if available, default is True.

    Returns:
    - **list[Union[YoutubeVideoWithCommentsDTO, YoutubeVideoWithCommentsAndTranscriptSchema,
    ErrorDTO]]**:
        A schema containing a list of video details with associated comments and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        channel=channel,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        use_cache=use_cache,
        engine=engine,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    channel: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
    ]
]:
    """Get Video And Comments By Query

     Retrieves YouTube videos and their comments based on a channel search query.

    This endpoint fetches YouTube videos and their associated comments for a specific channel
    based on the query provided. It uses stop triggers to control the number of posts retrieved
    and the maximum duration for the process. Caching is available to reduce redundant requests.

    Args:
    - **channel**: The channel name to query YouTube videos from, example is 'Formula1'.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of posts to retrieve, default is 5.
    - **max_duration_sec**: The maximum duration for retrieving data in seconds, default is 60.
    - **use_cache**: Boolean flag indicating whether to use cached data if available, default is True.

    Returns:
    - **list[Union[YoutubeVideoWithCommentsDTO, YoutubeVideoWithCommentsAndTranscriptSchema,
    ErrorDTO]]**:
        A schema containing a list of video details with associated comments and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO]
    """

    return sync_detailed(
        client=client,
        channel=channel,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        use_cache=use_cache,
        engine=engine,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    channel: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
    ]
]:
    """Get Video And Comments By Query

     Retrieves YouTube videos and their comments based on a channel search query.

    This endpoint fetches YouTube videos and their associated comments for a specific channel
    based on the query provided. It uses stop triggers to control the number of posts retrieved
    and the maximum duration for the process. Caching is available to reduce redundant requests.

    Args:
    - **channel**: The channel name to query YouTube videos from, example is 'Formula1'.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of posts to retrieve, default is 5.
    - **max_duration_sec**: The maximum duration for retrieving data in seconds, default is 60.
    - **use_cache**: Boolean flag indicating whether to use cached data if available, default is True.

    Returns:
    - **list[Union[YoutubeVideoWithCommentsDTO, YoutubeVideoWithCommentsAndTranscriptSchema,
    ErrorDTO]]**:
        A schema containing a list of video details with associated comments and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        channel=channel,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        use_cache=use_cache,
        engine=engine,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    channel: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO,
    ]
]:
    """Get Video And Comments By Query

     Retrieves YouTube videos and their comments based on a channel search query.

    This endpoint fetches YouTube videos and their associated comments for a specific channel
    based on the query provided. It uses stop triggers to control the number of posts retrieved
    and the maximum duration for the process. Caching is available to reduce redundant requests.

    Args:
    - **channel**: The channel name to query YouTube videos from, example is 'Formula1'.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of posts to retrieve, default is 5.
    - **max_duration_sec**: The maximum duration for retrieving data in seconds, default is 60.
    - **use_cache**: Boolean flag indicating whether to use cached data if available, default is True.

    Returns:
    - **list[Union[YoutubeVideoWithCommentsDTO, YoutubeVideoWithCommentsAndTranscriptSchema,
    ErrorDTO]]**:
        A schema containing a list of video details with associated comments and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        channel (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoWithCommentsDTOYoutubeVideoWithCommentsAndTranscriptSchemaErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            channel=channel,
            with_transcript=with_transcript,
            total_posts=total_posts,
            max_duration_sec=max_duration_sec,
            use_cache=use_cache,
            engine=engine,
        )
    ).parsed
