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
    url_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_extract_method: Union[Unset, str] = UNSET
    if not isinstance(extract_method, Unset):
        json_extract_method = extract_method.value

    params["extract_method"] = json_extract_method

    params["url"] = url_query

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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/collector/youtube/channels/videos",
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
    url_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[HTTPValidationError]:
    """Channel Videos

     Fetches videos from a YouTube channel based on the provided channel URL.

    This endpoint retrieves videos from the specified YouTube channel and allows for filtering by post
    timestamp.
    You can also limit the total number of posts and set a maximum duration for the extraction.

    Args:
    - **extract_method**: The method of extraction (e.g., API). Default is API.
    - **url**: The URL of the YouTube channel to extract videos from.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of videos to retrieve. Default is 5.
    - **max_duration_sec**: Maximum time in seconds for extracting data. Default is 60.
    - **post_timestamp**: Optional timestamp to filter videos created after this date.

    Returns:
    - **list[YoutubeVideoWithCommentsSchema | YoutubeVideoWithCommentsAndTranscriptSchema |
    GatewayErrorDTO]**: A list of videos or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        url_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
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
        url_query=url_query,
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
    url_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[HTTPValidationError]:
    """Channel Videos

     Fetches videos from a YouTube channel based on the provided channel URL.

    This endpoint retrieves videos from the specified YouTube channel and allows for filtering by post
    timestamp.
    You can also limit the total number of posts and set a maximum duration for the extraction.

    Args:
    - **extract_method**: The method of extraction (e.g., API). Default is API.
    - **url**: The URL of the YouTube channel to extract videos from.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of videos to retrieve. Default is 5.
    - **max_duration_sec**: Maximum time in seconds for extracting data. Default is 60.
    - **post_timestamp**: Optional timestamp to filter videos created after this date.

    Returns:
    - **list[YoutubeVideoWithCommentsSchema | YoutubeVideoWithCommentsAndTranscriptSchema |
    GatewayErrorDTO]**: A list of videos or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        url_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
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
        url_query=url_query,
        with_transcript=with_transcript,
        total_posts=total_posts,
        max_duration_sec=max_duration_sec,
        post_timestamp=post_timestamp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    url_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[HTTPValidationError]:
    """Channel Videos

     Fetches videos from a YouTube channel based on the provided channel URL.

    This endpoint retrieves videos from the specified YouTube channel and allows for filtering by post
    timestamp.
    You can also limit the total number of posts and set a maximum duration for the extraction.

    Args:
    - **extract_method**: The method of extraction (e.g., API). Default is API.
    - **url**: The URL of the YouTube channel to extract videos from.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of videos to retrieve. Default is 5.
    - **max_duration_sec**: Maximum time in seconds for extracting data. Default is 60.
    - **post_timestamp**: Optional timestamp to filter videos created after this date.

    Returns:
    - **list[YoutubeVideoWithCommentsSchema | YoutubeVideoWithCommentsAndTranscriptSchema |
    GatewayErrorDTO]**: A list of videos or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        url_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
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
        url_query=url_query,
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
    url_query: str,
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    max_duration_sec: Union[Unset, int] = 60,
    post_timestamp: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[HTTPValidationError]:
    """Channel Videos

     Fetches videos from a YouTube channel based on the provided channel URL.

    This endpoint retrieves videos from the specified YouTube channel and allows for filtering by post
    timestamp.
    You can also limit the total number of posts and set a maximum duration for the extraction.

    Args:
    - **extract_method**: The method of extraction (e.g., API). Default is API.
    - **url**: The URL of the YouTube channel to extract videos from.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The maximum number of videos to retrieve. Default is 5.
    - **max_duration_sec**: Maximum time in seconds for extracting data. Default is 60.
    - **post_timestamp**: Optional timestamp to filter videos created after this date.

    Returns:
    - **list[YoutubeVideoWithCommentsSchema | YoutubeVideoWithCommentsAndTranscriptSchema |
    GatewayErrorDTO]**: A list of videos or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        url_query (str):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
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
            url_query=url_query,
            with_transcript=with_transcript,
            total_posts=total_posts,
            max_duration_sec=max_duration_sec,
            post_timestamp=post_timestamp,
        )
    ).parsed
