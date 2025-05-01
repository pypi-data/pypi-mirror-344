from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_paginated_response_workflow_dto import (
    ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workflow_name: Union[None, Unset, str] = UNSET,
    project_id: Union[None, UUID, Unset] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_workflow_name: Union[None, Unset, str]
    if isinstance(workflow_name, Unset):
        json_workflow_name = UNSET
    else:
        json_workflow_name = workflow_name
    params["workflow_name"] = json_workflow_name

    json_project_id: Union[None, Unset, str]
    if isinstance(project_id, Unset):
        json_project_id = UNSET
    elif isinstance(project_id, UUID):
        json_project_id = str(project_id)
    else:
        json_project_id = project_id
    params["project_id"] = json_project_id

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/workflows",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    workflow_name: Union[None, Unset, str] = UNSET,
    project_id: Union[None, UUID, Unset] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]:
    """Get Workflows

     Retrieve a paginated list of workflows for the authenticated user.

    Args:
    - **workflow_name**: Filter workflows by name.
    - **project_id**: Filter workflows by project ID.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowDTO]**: A paginated list of workflows.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        workflow_name (Union[None, Unset, str]):
        project_id (Union[None, UUID, Unset]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]
    """

    kwargs = _get_kwargs(
        workflow_name=workflow_name,
        project_id=project_id,
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
    workflow_name: Union[None, Unset, str] = UNSET,
    project_id: Union[None, UUID, Unset] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]:
    """Get Workflows

     Retrieve a paginated list of workflows for the authenticated user.

    Args:
    - **workflow_name**: Filter workflows by name.
    - **project_id**: Filter workflows by project ID.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowDTO]**: A paginated list of workflows.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        workflow_name (Union[None, Unset, str]):
        project_id (Union[None, UUID, Unset]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]
    """

    return sync_detailed(
        client=client,
        workflow_name=workflow_name,
        project_id=project_id,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    workflow_name: Union[None, Unset, str] = UNSET,
    project_id: Union[None, UUID, Unset] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]:
    """Get Workflows

     Retrieve a paginated list of workflows for the authenticated user.

    Args:
    - **workflow_name**: Filter workflows by name.
    - **project_id**: Filter workflows by project ID.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowDTO]**: A paginated list of workflows.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        workflow_name (Union[None, Unset, str]):
        project_id (Union[None, UUID, Unset]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]
    """

    kwargs = _get_kwargs(
        workflow_name=workflow_name,
        project_id=project_id,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    workflow_name: Union[None, Unset, str] = UNSET,
    project_id: Union[None, UUID, Unset] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]]:
    """Get Workflows

     Retrieve a paginated list of workflows for the authenticated user.

    Args:
    - **workflow_name**: Filter workflows by name.
    - **project_id**: Filter workflows by project ID.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowDTO]**: A paginated list of workflows.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.

    Args:
        workflow_name (Union[None, Unset, str]):
        project_id (Union[None, UUID, Unset]):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPaginatedResponseWorkflowDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            workflow_name=workflow_name,
            project_id=project_id,
            page=page,
            per_page=per_page,
        )
    ).parsed
