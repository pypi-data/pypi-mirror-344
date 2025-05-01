from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.youtube_video_schema import YoutubeVideoSchema
from ...types import Response


def _get_kwargs(
    channel_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/channels/{channel_id}/videos/top",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, YoutubeVideoSchema]]:
    if response.status_code == 200:
        response_200 = YoutubeVideoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, YoutubeVideoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, YoutubeVideoSchema]]:
    """Get Top Channel Video

     Get the top video by views for a specific YouTube channel.

    This endpoint retrieves the video with the highest number of views from the specified YouTube
    channel.

    Args:
    - **channel_id**: The UUID of the YouTube channel to fetch the top video from.

    Returns:
    - **YoutubeVideoSchema**: A schema containing information about the top YouTube video.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    channel.

    Args:
        channel_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, YoutubeVideoSchema]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, YoutubeVideoSchema]]:
    """Get Top Channel Video

     Get the top video by views for a specific YouTube channel.

    This endpoint retrieves the video with the highest number of views from the specified YouTube
    channel.

    Args:
    - **channel_id**: The UUID of the YouTube channel to fetch the top video from.

    Returns:
    - **YoutubeVideoSchema**: A schema containing information about the top YouTube video.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    channel.

    Args:
        channel_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, YoutubeVideoSchema]
    """

    return sync_detailed(
        channel_id=channel_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, YoutubeVideoSchema]]:
    """Get Top Channel Video

     Get the top video by views for a specific YouTube channel.

    This endpoint retrieves the video with the highest number of views from the specified YouTube
    channel.

    Args:
    - **channel_id**: The UUID of the YouTube channel to fetch the top video from.

    Returns:
    - **YoutubeVideoSchema**: A schema containing information about the top YouTube video.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    channel.

    Args:
        channel_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, YoutubeVideoSchema]]
    """

    kwargs = _get_kwargs(
        channel_id=channel_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    channel_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, YoutubeVideoSchema]]:
    """Get Top Channel Video

     Get the top video by views for a specific YouTube channel.

    This endpoint retrieves the video with the highest number of views from the specified YouTube
    channel.

    Args:
    - **channel_id**: The UUID of the YouTube channel to fetch the top video from.

    Returns:
    - **YoutubeVideoSchema**: A schema containing information about the top YouTube video.

    Raises:
    - **404 Not Found (VideoResultNotFoundException)**: Raised if no videos are found for the given
    channel.

    Args:
        channel_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, YoutubeVideoSchema]
    """

    return (
        await asyncio_detailed(
            channel_id=channel_id,
            client=client,
        )
    ).parsed
