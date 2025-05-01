from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_paginated_response_project_get_schema import (
    ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    project_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_project_name: Union[None, Unset, str]
    if isinstance(project_name, Unset):
        json_project_name = UNSET
    else:
        json_project_name = project_name
    params["project_name"] = json_project_name

    params["page"] = page

    params["per_page"] = per_page

    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]:
    """Get Projects

     Retrieve a paginated list of projects for the authenticated user.

    Args:
    - **project_name**: Filter projects by name.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).
    - **q[str]**: General search query for filtering projects.

    Returns:
    - **PaginatedResponse[ProjectGetSchema]**: A paginated list of projects.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        project_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        page=page,
        per_page=per_page,
        q=q,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]:
    """Get Projects

     Retrieve a paginated list of projects for the authenticated user.

    Args:
    - **project_name**: Filter projects by name.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).
    - **q[str]**: General search query for filtering projects.

    Returns:
    - **PaginatedResponse[ProjectGetSchema]**: A paginated list of projects.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        project_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]
    """

    return sync_detailed(
        client=client,
        project_name=project_name,
        page=page,
        per_page=per_page,
        q=q,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]:
    """Get Projects

     Retrieve a paginated list of projects for the authenticated user.

    Args:
    - **project_name**: Filter projects by name.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).
    - **q[str]**: General search query for filtering projects.

    Returns:
    - **PaginatedResponse[ProjectGetSchema]**: A paginated list of projects.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        project_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]
    """

    kwargs = _get_kwargs(
        project_name=project_name,
        page=page,
        per_page=per_page,
        q=q,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_name: Union[None, Unset, str] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
    q: Union[Unset, str] = "",
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]]:
    """Get Projects

     Retrieve a paginated list of projects for the authenticated user.

    Args:
    - **project_name**: Filter projects by name.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).
    - **q[str]**: General search query for filtering projects.

    Returns:
    - **PaginatedResponse[ProjectGetSchema]**: A paginated list of projects.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        project_name (Union[None, Unset, str]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.
        q (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseProjectGetSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            project_name=project_name,
            page=page,
            per_page=per_page,
            q=q,
        )
    ).parsed
