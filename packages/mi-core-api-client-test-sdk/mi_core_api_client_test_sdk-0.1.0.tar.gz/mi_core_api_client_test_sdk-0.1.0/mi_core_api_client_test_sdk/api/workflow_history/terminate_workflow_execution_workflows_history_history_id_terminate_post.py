from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    history_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/workflows/history/{history_id}/terminate",
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
    history_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError]:
    """Terminate Workflow Execution

     Terminate a workflow execution by its history ID for the authenticated user.

    Args:
    - **history_id**: The history ID of the workflow execution to terminate.

    Returns:
    - **WorkflowHistoryDTO**: The details of the terminated workflow execution.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found (WorkflowNotFound)**: Raised if the workflow execution history does not exist or
    is inaccessible by the user.
    - **400 Bad Request (WorkflowTerminationError)**: Raised if the workflow execution cannot be
    terminated.

    Args:
        history_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        history_id=history_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    history_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[HTTPValidationError]:
    """Terminate Workflow Execution

     Terminate a workflow execution by its history ID for the authenticated user.

    Args:
    - **history_id**: The history ID of the workflow execution to terminate.

    Returns:
    - **WorkflowHistoryDTO**: The details of the terminated workflow execution.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found (WorkflowNotFound)**: Raised if the workflow execution history does not exist or
    is inaccessible by the user.
    - **400 Bad Request (WorkflowTerminationError)**: Raised if the workflow execution cannot be
    terminated.

    Args:
        history_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        history_id=history_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    history_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError]:
    """Terminate Workflow Execution

     Terminate a workflow execution by its history ID for the authenticated user.

    Args:
    - **history_id**: The history ID of the workflow execution to terminate.

    Returns:
    - **WorkflowHistoryDTO**: The details of the terminated workflow execution.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found (WorkflowNotFound)**: Raised if the workflow execution history does not exist or
    is inaccessible by the user.
    - **400 Bad Request (WorkflowTerminationError)**: Raised if the workflow execution cannot be
    terminated.

    Args:
        history_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        history_id=history_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    history_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[HTTPValidationError]:
    """Terminate Workflow Execution

     Terminate a workflow execution by its history ID for the authenticated user.

    Args:
    - **history_id**: The history ID of the workflow execution to terminate.

    Returns:
    - **WorkflowHistoryDTO**: The details of the terminated workflow execution.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found (WorkflowNotFound)**: Raised if the workflow execution history does not exist or
    is inaccessible by the user.
    - **400 Bad Request (WorkflowTerminationError)**: Raised if the workflow execution cannot be
    terminated.

    Args:
        history_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            history_id=history_id,
            client=client,
        )
    ).parsed
