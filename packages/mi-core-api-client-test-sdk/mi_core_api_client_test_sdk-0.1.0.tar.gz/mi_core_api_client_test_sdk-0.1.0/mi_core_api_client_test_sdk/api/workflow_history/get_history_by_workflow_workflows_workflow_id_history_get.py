from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workflow_id: UUID,
    *,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/workflows/{workflow_id}/history",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[HTTPValidationError]:
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workflow_id: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Response[HTTPValidationError]:
    """Get History By Workflow

     Retrieve a paginated list of workflow execution history for a specific workflow.

    Args:
    - **workflow_id**: The ID of the workflow to retrieve history for.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowHistoryDTO]**: A paginated list of workflow execution history.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found(WorkflowNotFound)**: Raised if the workflow does not exist or is inaccessible by
    the user.

    Args:
        workflow_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workflow_id: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Optional[HTTPValidationError]:
    """Get History By Workflow

     Retrieve a paginated list of workflow execution history for a specific workflow.

    Args:
    - **workflow_id**: The ID of the workflow to retrieve history for.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowHistoryDTO]**: A paginated list of workflow execution history.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found(WorkflowNotFound)**: Raised if the workflow does not exist or is inaccessible by
    the user.

    Args:
        workflow_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        workflow_id=workflow_id,
        client=client,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    workflow_id: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Response[HTTPValidationError]:
    """Get History By Workflow

     Retrieve a paginated list of workflow execution history for a specific workflow.

    Args:
    - **workflow_id**: The ID of the workflow to retrieve history for.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowHistoryDTO]**: A paginated list of workflow execution history.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found(WorkflowNotFound)**: Raised if the workflow does not exist or is inaccessible by
    the user.

    Args:
        workflow_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workflow_id: UUID,
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 5,
) -> Optional[HTTPValidationError]:
    """Get History By Workflow

     Retrieve a paginated list of workflow execution history for a specific workflow.

    Args:
    - **workflow_id**: The ID of the workflow to retrieve history for.
    - **page**: Page number for pagination (default: 1, minimum: 1).
    - **per_page**: Number of items per page for pagination (default: 5, maximum: 25).

    Returns:
    - **PaginatedResponse[WorkflowHistoryDTO]**: A paginated list of workflow execution history.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found(WorkflowNotFound)**: Raised if the workflow does not exist or is inaccessible by
    the user.

    Args:
        workflow_id (UUID):
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            client=client,
            page=page,
            per_page=per_page,
        )
    ).parsed
