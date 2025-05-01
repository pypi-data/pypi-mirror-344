import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto import (
    ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    channel: str,
    search_query: Union[Unset, str] = UNSET,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["channel"] = channel

    params["search_query"] = search_query

    params["with_transcript"] = with_transcript

    params["total_posts"] = total_posts

    params["max_duration_sec"] = max_duration_sec

    json_post_timestamp: Union[None, Unset, str]
    if isinstance(post_timestamp, Unset):
        json_post_timestamp = UNSET
    elif isinstance(post_timestamp, datetime.datetime):
        json_post_timestamp = post_timestamp.isoformat()
    else:
        json_post_timestamp = post_timestamp
    params["post_timestamp"] = json_post_timestamp

    params["use_cache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/youtube/channels/videos",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    if response.status_code == 200:
        response_200 = (
            ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO.from_dict(
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
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
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
    search_query: Union[Unset, str] = UNSET,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Channel

     Retrieves YouTube videos for a specific channel.

    This endpoint fetches YouTube videos from a given channel, supporting filters
    like timestamps and total posts, along with caching to reduce redundant requests.

    Args:
    - **channel**: The name of the YouTube channel to retrieve videos from.
    - **search_query**: The search query to filter videos by, default is None.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The number of posts to retrieve, default is 5.
    - **max_duration_sec**: Maximum allowed time for video extraction in seconds, default is 60.
    - **post_timestamp**: A timestamp to filter videos created after this date.
    - **use_cache**: Boolean indicating whether to use cached results, default is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing video details and error information if any.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
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
        search_query (Union[Unset, str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter videos created
            after this date
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]]
    """

    kwargs = _get_kwargs(
        channel=channel,
        search_query=search_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    channel: str,
    search_query: Union[Unset, str] = UNSET,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Channel

     Retrieves YouTube videos for a specific channel.

    This endpoint fetches YouTube videos from a given channel, supporting filters
    like timestamps and total posts, along with caching to reduce redundant requests.

    Args:
    - **channel**: The name of the YouTube channel to retrieve videos from.
    - **search_query**: The search query to filter videos by, default is None.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The number of posts to retrieve, default is 5.
    - **max_duration_sec**: Maximum allowed time for video extraction in seconds, default is 60.
    - **post_timestamp**: A timestamp to filter videos created after this date.
    - **use_cache**: Boolean indicating whether to use cached results, default is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing video details and error information if any.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
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
        search_query (Union[Unset, str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter videos created
            after this date
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]
    """

    return sync_detailed(
        client=client,
        channel=channel,
        search_query=search_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    channel: str,
    search_query: Union[Unset, str] = UNSET,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Channel

     Retrieves YouTube videos for a specific channel.

    This endpoint fetches YouTube videos from a given channel, supporting filters
    like timestamps and total posts, along with caching to reduce redundant requests.

    Args:
    - **channel**: The name of the YouTube channel to retrieve videos from.
    - **search_query**: The search query to filter videos by, default is None.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The number of posts to retrieve, default is 5.
    - **max_duration_sec**: Maximum allowed time for video extraction in seconds, default is 60.
    - **post_timestamp**: A timestamp to filter videos created after this date.
    - **use_cache**: Boolean indicating whether to use cached results, default is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing video details and error information if any.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
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
        search_query (Union[Unset, str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter videos created
            after this date
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]]
    """

    kwargs = _get_kwargs(
        channel=channel,
        search_query=search_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    channel: str,
    search_query: Union[Unset, str] = UNSET,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
    use_cache: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Channel

     Retrieves YouTube videos for a specific channel.

    This endpoint fetches YouTube videos from a given channel, supporting filters
    like timestamps and total posts, along with caching to reduce redundant requests.

    Args:
    - **channel**: The name of the YouTube channel to retrieve videos from.
    - **search_query**: The search query to filter videos by, default is None.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The number of posts to retrieve, default is 5.
    - **max_duration_sec**: Maximum allowed time for video extraction in seconds, default is 60.
    - **post_timestamp**: A timestamp to filter videos created after this date.
    - **use_cache**: Boolean indicating whether to use cached results, default is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing video details and error information if any.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
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
        search_query (Union[Unset, str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter videos created
            after this date
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            channel=channel,
            search_query=search_query,
            with_transcript=with_transcript,
            total_posts=total_posts,
            max_duration_sec=max_duration_sec,
            post_timestamp=post_timestamp,
            use_cache=use_cache,
        )
    ).parsed
