from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_type import PromptType
from ...models.response_with_metadata_schema_paginated_response_prompt_info_schema import (
    ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    prompt_type: PromptType,
    title: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_prompt_type = prompt_type.value
    params["prompt_type"] = json_prompt_type

    json_title: Union[None, Unset, str]
    if isinstance(title, Unset):
        json_title = UNSET
    else:
        json_title = title
    params["title"] = json_title

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/prompts",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    prompt_type: PromptType,
    title: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]:
    """Get All Prompt

     Retrieve all prompts with optional filters.

    This endpoint allows superusers or moderators to fetch a paginated list of prompts, optionally
    filtered by type or title.

    Args:
    - **prompt_type[PromptType]**: Filter by prompt type (default: storyboard_generation).
    - **title**: Filter by title.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 10, maximum: 100).

    Returns:
    - **PaginatedResponse[PromptInfoSchema]**: A paginated list of prompts.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.
        title (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_type=prompt_type,
        title=title,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    prompt_type: PromptType,
    title: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]:
    """Get All Prompt

     Retrieve all prompts with optional filters.

    This endpoint allows superusers or moderators to fetch a paginated list of prompts, optionally
    filtered by type or title.

    Args:
    - **prompt_type[PromptType]**: Filter by prompt type (default: storyboard_generation).
    - **title**: Filter by title.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 10, maximum: 100).

    Returns:
    - **PaginatedResponse[PromptInfoSchema]**: A paginated list of prompts.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.
        title (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]
    """

    return sync_detailed(
        client=client,
        prompt_type=prompt_type,
        title=title,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    prompt_type: PromptType,
    title: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]:
    """Get All Prompt

     Retrieve all prompts with optional filters.

    This endpoint allows superusers or moderators to fetch a paginated list of prompts, optionally
    filtered by type or title.

    Args:
    - **prompt_type[PromptType]**: Filter by prompt type (default: storyboard_generation).
    - **title**: Filter by title.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 10, maximum: 100).

    Returns:
    - **PaginatedResponse[PromptInfoSchema]**: A paginated list of prompts.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.
        title (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_type=prompt_type,
        title=title,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    prompt_type: PromptType,
    title: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]]:
    """Get All Prompt

     Retrieve all prompts with optional filters.

    This endpoint allows superusers or moderators to fetch a paginated list of prompts, optionally
    filtered by type or title.

    Args:
    - **prompt_type[PromptType]**: Filter by prompt type (default: storyboard_generation).
    - **title**: Filter by title.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 10, maximum: 100).

    Returns:
    - **PaginatedResponse[PromptInfoSchema]**: A paginated list of prompts.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.
        title (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponsePromptInfoSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            prompt_type=prompt_type,
            title=title,
            page=page,
            per_page=per_page,
        )
    ).parsed
