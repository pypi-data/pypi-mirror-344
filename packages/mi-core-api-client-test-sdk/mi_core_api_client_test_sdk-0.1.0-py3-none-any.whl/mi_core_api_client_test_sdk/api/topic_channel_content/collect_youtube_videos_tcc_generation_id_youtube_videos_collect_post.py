from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_collect_youtube_videos_data import (
    ResponseWithMetadataSchemaCollectYoutubeVideosData,
)
from ...models.youtube_videos_request import YoutubeVideosRequest
from ...types import Response


def _get_kwargs(
    generation_id: UUID,
    *,
    body: YoutubeVideosRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/tcc/{generation_id}/youtube-videos/collect",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaCollectYoutubeVideosData.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    generation_id: UUID,
    *,
    client: AuthenticatedClient,
    body: YoutubeVideosRequest,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]:
    """Collect Youtube Videos

    Args:
        generation_id (UUID):
        body (YoutubeVideosRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]
    """

    kwargs = _get_kwargs(
        generation_id=generation_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    generation_id: UUID,
    *,
    client: AuthenticatedClient,
    body: YoutubeVideosRequest,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]:
    """Collect Youtube Videos

    Args:
        generation_id (UUID):
        body (YoutubeVideosRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]
    """

    return sync_detailed(
        generation_id=generation_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    generation_id: UUID,
    *,
    client: AuthenticatedClient,
    body: YoutubeVideosRequest,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]:
    """Collect Youtube Videos

    Args:
        generation_id (UUID):
        body (YoutubeVideosRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]
    """

    kwargs = _get_kwargs(
        generation_id=generation_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    generation_id: UUID,
    *,
    client: AuthenticatedClient,
    body: YoutubeVideosRequest,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]]:
    """Collect Youtube Videos

    Args:
        generation_id (UUID):
        body (YoutubeVideosRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCollectYoutubeVideosData]
    """

    return (
        await asyncio_detailed(
            generation_id=generation_id,
            client=client,
            body=body,
        )
    ).parsed
