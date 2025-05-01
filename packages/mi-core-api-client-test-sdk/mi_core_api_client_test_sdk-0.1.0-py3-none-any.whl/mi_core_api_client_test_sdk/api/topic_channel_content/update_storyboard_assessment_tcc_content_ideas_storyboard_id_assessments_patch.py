from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_storyboard_assessment_response import (
    ResponseWithMetadataSchemaStoryboardAssessmentResponse,
)
from ...models.storyboard_assessment_request import StoryboardAssessmentRequest
from ...types import Response


def _get_kwargs(
    storyboard_id: UUID,
    *,
    body: StoryboardAssessmentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/tcc/content-ideas/{storyboard_id}/assessments",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaStoryboardAssessmentResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: StoryboardAssessmentRequest,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]:
    """Update Storyboard Assessment

    Args:
        storyboard_id (UUID):
        body (StoryboardAssessmentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]
    """

    kwargs = _get_kwargs(
        storyboard_id=storyboard_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: StoryboardAssessmentRequest,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]:
    """Update Storyboard Assessment

    Args:
        storyboard_id (UUID):
        body (StoryboardAssessmentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]
    """

    return sync_detailed(
        storyboard_id=storyboard_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: StoryboardAssessmentRequest,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]:
    """Update Storyboard Assessment

    Args:
        storyboard_id (UUID):
        body (StoryboardAssessmentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]
    """

    kwargs = _get_kwargs(
        storyboard_id=storyboard_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: StoryboardAssessmentRequest,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]]:
    """Update Storyboard Assessment

    Args:
        storyboard_id (UUID):
        body (StoryboardAssessmentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaStoryboardAssessmentResponse]
    """

    return (
        await asyncio_detailed(
            storyboard_id=storyboard_id,
            client=client,
            body=body,
        )
    ).parsed
