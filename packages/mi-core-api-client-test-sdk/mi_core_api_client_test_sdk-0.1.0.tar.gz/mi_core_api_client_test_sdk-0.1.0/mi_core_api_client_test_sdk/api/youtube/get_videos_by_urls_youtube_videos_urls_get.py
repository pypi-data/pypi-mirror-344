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
    urls: list[str],
    with_transcript: Union[Unset, bool] = False,
    use_cache: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_urls = urls

    params["urls"] = json_urls

    params["with_transcript"] = with_transcript

    params["use_cache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/youtube/videos/urls",
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
    urls: list[str],
    with_transcript: Union[Unset, bool] = False,
    use_cache: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Urls

     Retrieves videos and optionally comments from YouTube by the provided URLs.

    This endpoint fetches YouTube video details, optionally including comments, based on a list of
    provided URLs.
    It uses caching to optimize the process and reduce the number of external requests.

    Args:
    - **urls**: A list of YouTube video URLs for which to retrieve video details and comments.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **use_cache**: Boolean flag indicating whether to use cached data for the requested URLs, default
    is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing the list of retrieved YouTube video information and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
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
        urls (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]]
    """

    kwargs = _get_kwargs(
        urls=urls,
        with_transcript=with_transcript,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    urls: list[str],
    with_transcript: Union[Unset, bool] = False,
    use_cache: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Urls

     Retrieves videos and optionally comments from YouTube by the provided URLs.

    This endpoint fetches YouTube video details, optionally including comments, based on a list of
    provided URLs.
    It uses caching to optimize the process and reduce the number of external requests.

    Args:
    - **urls**: A list of YouTube video URLs for which to retrieve video details and comments.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **use_cache**: Boolean flag indicating whether to use cached data for the requested URLs, default
    is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing the list of retrieved YouTube video information and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
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
        urls (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]
    """

    return sync_detailed(
        client=client,
        urls=urls,
        with_transcript=with_transcript,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    urls: list[str],
    with_transcript: Union[Unset, bool] = False,
    use_cache: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Urls

     Retrieves videos and optionally comments from YouTube by the provided URLs.

    This endpoint fetches YouTube video details, optionally including comments, based on a list of
    provided URLs.
    It uses caching to optimize the process and reduce the number of external requests.

    Args:
    - **urls**: A list of YouTube video URLs for which to retrieve video details and comments.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **use_cache**: Boolean flag indicating whether to use cached data for the requested URLs, default
    is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing the list of retrieved YouTube video information and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
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
        urls (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
        use_cache (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO]]
    """

    kwargs = _get_kwargs(
        urls=urls,
        with_transcript=with_transcript,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    urls: list[str],
    with_transcript: Union[Unset, bool] = False,
    use_cache: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeVideoSchemaYoutubeVideoWithTranscriptDTOErrorDTO
    ]
]:
    """Get Videos By Urls

     Retrieves videos and optionally comments from YouTube by the provided URLs.

    This endpoint fetches YouTube video details, optionally including comments, based on a list of
    provided URLs.
    It uses caching to optimize the process and reduce the number of external requests.

    Args:
    - **urls**: A list of YouTube video URLs for which to retrieve video details and comments.
    - **with_transcript**: Whether to include the transcript of the video or not, default is False.
    - **use_cache**: Boolean flag indicating whether to use cached data for the requested URLs, default
    is True.

    Returns:
    - **list[Union[YoutubeVideoSchema, YoutubeVideoWithTranscriptDTO, ErrorDTO]]**:
        A schema containing the list of retrieved YouTube video information and any errors encountered.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    URLs.
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
        urls (list[str]):
        with_transcript (Union[Unset, bool]):  Default: False.
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
            urls=urls,
            with_transcript=with_transcript,
            use_cache=use_cache,
        )
    ).parsed
