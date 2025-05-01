from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_youtube_video_schema_youtube_video_with_transcript_dto_error_dto import (
    ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO,
)
from ...models.serp_search_engine import SerpSearchEngine
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    queries: list[str],
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_queries = queries

    params["queries"] = json_queries

    params["with_transcript"] = with_transcript

    params["total_posts"] = total_posts

    params["use_cache"] = use_cache

    json_engine: Union[Unset, str] = UNSET
    if not isinstance(engine, Unset):
        json_engine = engine.value

    params["engine"] = json_engine

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/youtube/videos",
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
    queries: list[str],
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Queries

     Get YouTube videos based on provided queries.

    This endpoint allows searching for YouTube videos by providing a list of queries. The search
    results can be limited by the number of videos, and the results can be fetched from cache if
    available.

    Args:
    - **queries**: A list of queries to search for videos.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The total number of videos to fetch for each query, default is 5.
    - **use_cache**: Boolean flag indicating whether to use cached results if available.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**: A list of YouTube
    videos matching the search criteria.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the provided
    query.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction fails during the
    process.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        queries (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        with_transcript=with_transcript,
        total_posts=total_posts,
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
    queries: list[str],
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Queries

     Get YouTube videos based on provided queries.

    This endpoint allows searching for YouTube videos by providing a list of queries. The search
    results can be limited by the number of videos, and the results can be fetched from cache if
    available.

    Args:
    - **queries**: A list of queries to search for videos.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The total number of videos to fetch for each query, default is 5.
    - **use_cache**: Boolean flag indicating whether to use cached results if available.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**: A list of YouTube
    videos matching the search criteria.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the provided
    query.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction fails during the
    process.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        queries (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]
    """

    return sync_detailed(
        client=client,
        queries=queries,
        with_transcript=with_transcript,
        total_posts=total_posts,
        use_cache=use_cache,
        engine=engine,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Queries

     Get YouTube videos based on provided queries.

    This endpoint allows searching for YouTube videos by providing a list of queries. The search
    results can be limited by the number of videos, and the results can be fetched from cache if
    available.

    Args:
    - **queries**: A list of queries to search for videos.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The total number of videos to fetch for each query, default is 5.
    - **use_cache**: Boolean flag indicating whether to use cached results if available.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**: A list of YouTube
    videos matching the search criteria.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the provided
    query.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction fails during the
    process.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        queries (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        with_transcript=with_transcript,
        total_posts=total_posts,
        use_cache=use_cache,
        engine=engine,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    with_transcript: Union[Unset, bool] = False,
    total_posts: Union[Unset, int] = 5,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Queries

     Get YouTube videos based on provided queries.

    This endpoint allows searching for YouTube videos by providing a list of queries. The search
    results can be limited by the number of videos, and the results can be fetched from cache if
    available.

    Args:
    - **queries**: A list of queries to search for videos.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **total_posts**: The total number of videos to fetch for each query, default is 5.
    - **use_cache**: Boolean flag indicating whether to use cached results if available.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**: A list of YouTube
    videos matching the search criteria.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the provided
    query.
    - **404 Not Found (ResultNotFoundException)**: Raised if no search results are found.
    - **429 Too Many Requests (RunOutOfSearchesException)**: Raised if the search quota has been
    exceeded during the search request.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if data extraction fails during the
    process.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        queries (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        total_posts (Union[Unset, int]):  Default: 5.
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            queries=queries,
            with_transcript=with_transcript,
            total_posts=total_posts,
            use_cache=use_cache,
            engine=engine,
        )
    ).parsed
