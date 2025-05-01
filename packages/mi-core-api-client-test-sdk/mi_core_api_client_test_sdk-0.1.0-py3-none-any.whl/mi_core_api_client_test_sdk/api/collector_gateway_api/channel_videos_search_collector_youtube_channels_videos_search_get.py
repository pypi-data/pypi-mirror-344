import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.extract_method import ExtractMethod
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    channel_name: str,
    search_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_extract_method: Union[Unset, str] = UNSET
    if not isinstance(extract_method, Unset):
        json_extract_method = extract_method.value

    params["extract_method"] = json_extract_method

    params["channel_name"] = channel_name

    params["search_query"] = search_query

    params["with_transcript"] = with_transcript

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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/collector/youtube/channels/videos/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[HTTPValidationError]:
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    channel_name: str,
    search_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[HTTPValidationError]:
    """Channel Videos Search

     Search YouTube videos by query in given channel name.

    Params:
        channel_name: The name of the YouTube channel to search videos in.
        search_query: The search query to search videos in the channel.
        total_posts: The total number of posts to fetch.
        max_duration_sec: The maximum duration in seconds for fetching the response.
        post_timestamp: The timestamp of the post to fetch until.
        extract_method: ExtractMethod enum value. Defaults to ExtractMethod.HTML.
        extractor: Extractor to use.

    Exceptions:
        400 InvalidAPIKeyError: If the API key is invalid.
        400 RunOutOfYoutubeAPIKey: If the Reddit credentials are invalid.
        404 YoutubeChannelNotFoundException: If the provided channel URLs is not found.
        500 FailedToExtractData: If all the provided URLs cannot be extracted.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        channel_name (str):
        search_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter channels
            videos created after this date

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        extract_method=extract_method,
        channel_name=channel_name,
        search_query=search_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    channel_name: str,
    search_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[HTTPValidationError]:
    """Channel Videos Search

     Search YouTube videos by query in given channel name.

    Params:
        channel_name: The name of the YouTube channel to search videos in.
        search_query: The search query to search videos in the channel.
        total_posts: The total number of posts to fetch.
        max_duration_sec: The maximum duration in seconds for fetching the response.
        post_timestamp: The timestamp of the post to fetch until.
        extract_method: ExtractMethod enum value. Defaults to ExtractMethod.HTML.
        extractor: Extractor to use.

    Exceptions:
        400 InvalidAPIKeyError: If the API key is invalid.
        400 RunOutOfYoutubeAPIKey: If the Reddit credentials are invalid.
        404 YoutubeChannelNotFoundException: If the provided channel URLs is not found.
        500 FailedToExtractData: If all the provided URLs cannot be extracted.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        channel_name (str):
        search_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter channels
            videos created after this date

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        client=client,
        extract_method=extract_method,
        channel_name=channel_name,
        search_query=search_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    channel_name: str,
    search_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[HTTPValidationError]:
    """Channel Videos Search

     Search YouTube videos by query in given channel name.

    Params:
        channel_name: The name of the YouTube channel to search videos in.
        search_query: The search query to search videos in the channel.
        total_posts: The total number of posts to fetch.
        max_duration_sec: The maximum duration in seconds for fetching the response.
        post_timestamp: The timestamp of the post to fetch until.
        extract_method: ExtractMethod enum value. Defaults to ExtractMethod.HTML.
        extractor: Extractor to use.

    Exceptions:
        400 InvalidAPIKeyError: If the API key is invalid.
        400 RunOutOfYoutubeAPIKey: If the Reddit credentials are invalid.
        404 YoutubeChannelNotFoundException: If the provided channel URLs is not found.
        500 FailedToExtractData: If all the provided URLs cannot be extracted.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        channel_name (str):
        search_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter channels
            videos created after this date

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        extract_method=extract_method,
        channel_name=channel_name,
        search_query=search_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    channel_name: str,
    search_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[None, Unset, int] = UNSET,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[HTTPValidationError]:
    """Channel Videos Search

     Search YouTube videos by query in given channel name.

    Params:
        channel_name: The name of the YouTube channel to search videos in.
        search_query: The search query to search videos in the channel.
        total_posts: The total number of posts to fetch.
        max_duration_sec: The maximum duration in seconds for fetching the response.
        post_timestamp: The timestamp of the post to fetch until.
        extract_method: ExtractMethod enum value. Defaults to ExtractMethod.HTML.
        extractor: Extractor to use.

    Exceptions:
        400 InvalidAPIKeyError: If the API key is invalid.
        400 RunOutOfYoutubeAPIKey: If the Reddit credentials are invalid.
        404 YoutubeChannelNotFoundException: If the provided channel URLs is not found.
        500 FailedToExtractData: If all the provided URLs cannot be extracted.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        channel_name (str):
        search_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[None, Unset, int]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        post_timestamp (Union[None, Unset, datetime.datetime]): Timestamp to filter channels
            videos created after this date

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            extract_method=extract_method,
            channel_name=channel_name,
            search_query=search_query,
            with_transcript=with_transcript,
            total_posts=total_posts,
            max_duration_sec=max_duration_sec,
            post_timestamp=post_timestamp,
        )
    ).parsed
