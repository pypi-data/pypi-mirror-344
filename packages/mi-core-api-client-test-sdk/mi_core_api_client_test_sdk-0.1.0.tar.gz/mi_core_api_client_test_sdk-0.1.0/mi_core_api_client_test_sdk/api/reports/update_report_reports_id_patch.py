from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.report_update_schema import ReportUpdateSchema
from ...models.response_with_metadata_schema_report_schema import ResponseWithMetadataSchemaReportSchema
from ...types import Response


def _get_kwargs(
    id: UUID,
    *,
    body: ReportUpdateSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/reports/{id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaReportSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ReportUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]:
    """Update Report

     Update report for the authenticated user.

    Args:
    - **id**: The ID of the report to be updated.
    - **request[ReportUpdateSchema]**: Schema containing the details of the report to be updated.

    Returns:
    - **ReportSchema**: The details of the newly created report.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided report details are invalid.
    - **404 Not Found (ProjectNotFound)**: Raised if project_id not found for current user.
    - **400 Bad Request (InvalidQueryForReport)**: Raised if the provided query is invalid
    - **400 Bad Request (UnsupportedDocumentType)**: Raised if the provided report type is not
    supported.
    - **409 Conflict (ReportAlreadyExistsException)**: Raised if the report with the same name already
    exists for the project.

    Args:
        id (UUID):
        body (ReportUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ReportUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]:
    """Update Report

     Update report for the authenticated user.

    Args:
    - **id**: The ID of the report to be updated.
    - **request[ReportUpdateSchema]**: Schema containing the details of the report to be updated.

    Returns:
    - **ReportSchema**: The details of the newly created report.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided report details are invalid.
    - **404 Not Found (ProjectNotFound)**: Raised if project_id not found for current user.
    - **400 Bad Request (InvalidQueryForReport)**: Raised if the provided query is invalid
    - **400 Bad Request (UnsupportedDocumentType)**: Raised if the provided report type is not
    supported.
    - **409 Conflict (ReportAlreadyExistsException)**: Raised if the report with the same name already
    exists for the project.

    Args:
        id (UUID):
        body (ReportUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ReportUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]:
    """Update Report

     Update report for the authenticated user.

    Args:
    - **id**: The ID of the report to be updated.
    - **request[ReportUpdateSchema]**: Schema containing the details of the report to be updated.

    Returns:
    - **ReportSchema**: The details of the newly created report.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided report details are invalid.
    - **404 Not Found (ProjectNotFound)**: Raised if project_id not found for current user.
    - **400 Bad Request (InvalidQueryForReport)**: Raised if the provided query is invalid
    - **400 Bad Request (UnsupportedDocumentType)**: Raised if the provided report type is not
    supported.
    - **409 Conflict (ReportAlreadyExistsException)**: Raised if the report with the same name already
    exists for the project.

    Args:
        id (UUID):
        body (ReportUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ReportUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]]:
    """Update Report

     Update report for the authenticated user.

    Args:
    - **id**: The ID of the report to be updated.
    - **request[ReportUpdateSchema]**: Schema containing the details of the report to be updated.

    Returns:
    - **ReportSchema**: The details of the newly created report.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided report details are invalid.
    - **404 Not Found (ProjectNotFound)**: Raised if project_id not found for current user.
    - **400 Bad Request (InvalidQueryForReport)**: Raised if the provided query is invalid
    - **400 Bad Request (UnsupportedDocumentType)**: Raised if the provided report type is not
    supported.
    - **409 Conflict (ReportAlreadyExistsException)**: Raised if the report with the same name already
    exists for the project.

    Args:
        id (UUID):
        body (ReportUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaReportSchema]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
