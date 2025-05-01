from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.storyboard_with_scenes_dto import StoryboardWithScenesDTO
from ...types import Response


def _get_kwargs(
    storyboard_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/storyboards/{storyboard_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, StoryboardWithScenesDTO]]:
    if response.status_code == 200:
        response_200 = StoryboardWithScenesDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, StoryboardWithScenesDTO]]:
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
) -> Response[Union[HTTPValidationError, StoryboardWithScenesDTO]]:
    """Get Generated Storyboard By Id

     Retrieve a generated storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard.

    Returns:
    - **StoryboardWithScenesDTO**: The generated storyboard details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.
    - **404 Not Found (StoryboardNotFoundException)**: Raised if the storyboard does not exist.

    Args:
        storyboard_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StoryboardWithScenesDTO]]
    """

    kwargs = _get_kwargs(
        storyboard_id=storyboard_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StoryboardWithScenesDTO]]:
    """Get Generated Storyboard By Id

     Retrieve a generated storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard.

    Returns:
    - **StoryboardWithScenesDTO**: The generated storyboard details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.
    - **404 Not Found (StoryboardNotFoundException)**: Raised if the storyboard does not exist.

    Args:
        storyboard_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StoryboardWithScenesDTO]
    """

    return sync_detailed(
        storyboard_id=storyboard_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StoryboardWithScenesDTO]]:
    """Get Generated Storyboard By Id

     Retrieve a generated storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard.

    Returns:
    - **StoryboardWithScenesDTO**: The generated storyboard details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.
    - **404 Not Found (StoryboardNotFoundException)**: Raised if the storyboard does not exist.

    Args:
        storyboard_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StoryboardWithScenesDTO]]
    """

    kwargs = _get_kwargs(
        storyboard_id=storyboard_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StoryboardWithScenesDTO]]:
    """Get Generated Storyboard By Id

     Retrieve a generated storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard.

    Returns:
    - **StoryboardWithScenesDTO**: The generated storyboard details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.
    - **404 Not Found (StoryboardNotFoundException)**: Raised if the storyboard does not exist.

    Args:
        storyboard_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StoryboardWithScenesDTO]
    """

    return (
        await asyncio_detailed(
            storyboard_id=storyboard_id,
            client=client,
        )
    ).parsed
