from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_storyboard_with_scenes_dto import PaginatedResponseStoryboardWithScenesDTO
from ...models.storyboard_generation_status_enum import StoryboardGenerationStatusEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    status: Union[None, StoryboardGenerationStatusEnum, Unset] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["per_page"] = per_page

    json_status: Union[None, Unset, str]
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, StoryboardGenerationStatusEnum):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/storyboards",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseStoryboardWithScenesDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    status: Union[None, StoryboardGenerationStatusEnum, Unset] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]:
    """Get All Storyboards

     Retrieve a paginated list of all storyboards. Only accessible by superusers.

    Args:
    - **page**: Page number for pagination.
    - **per_page**: Number of items per page for pagination.
    - **status[StoryboardGenerationStatusEnum | None]**: Filter storyboards by generation status.

    Returns:
    - **PaginatedResponse[StoryboardWithScenesDTO]**: A paginated list of all storyboards.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        status (Union[None, StoryboardGenerationStatusEnum, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    status: Union[None, StoryboardGenerationStatusEnum, Unset] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]:
    """Get All Storyboards

     Retrieve a paginated list of all storyboards. Only accessible by superusers.

    Args:
    - **page**: Page number for pagination.
    - **per_page**: Number of items per page for pagination.
    - **status[StoryboardGenerationStatusEnum | None]**: Filter storyboards by generation status.

    Returns:
    - **PaginatedResponse[StoryboardWithScenesDTO]**: A paginated list of all storyboards.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        status (Union[None, StoryboardGenerationStatusEnum, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]
    """

    return sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        status=status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    status: Union[None, StoryboardGenerationStatusEnum, Unset] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]:
    """Get All Storyboards

     Retrieve a paginated list of all storyboards. Only accessible by superusers.

    Args:
    - **page**: Page number for pagination.
    - **per_page**: Number of items per page for pagination.
    - **status[StoryboardGenerationStatusEnum | None]**: Filter storyboards by generation status.

    Returns:
    - **PaginatedResponse[StoryboardWithScenesDTO]**: A paginated list of all storyboards.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        status (Union[None, StoryboardGenerationStatusEnum, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    status: Union[None, StoryboardGenerationStatusEnum, Unset] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]]:
    """Get All Storyboards

     Retrieve a paginated list of all storyboards. Only accessible by superusers.

    Args:
    - **page**: Page number for pagination.
    - **per_page**: Number of items per page for pagination.
    - **status[StoryboardGenerationStatusEnum | None]**: Filter storyboards by generation status.

    Returns:
    - **PaginatedResponse[StoryboardWithScenesDTO]**: A paginated list of all storyboards.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        status (Union[None, StoryboardGenerationStatusEnum, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseStoryboardWithScenesDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            per_page=per_page,
            status=status,
        )
    ).parsed
