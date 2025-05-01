from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_union_project_with_sources_dto_project_with_reports_dto_project_with_all_relations_dto_project_base_schema import (
    ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: UUID,
    *,
    with_sources: Union[Unset, bool] = True,
    with_reports: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["with_sources"] = with_sources

    params["with_reports"] = with_reports

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
    ]
]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema.from_dict(
            response.json()
        )

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
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
    ]
]:
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
    with_sources: Union[Unset, bool] = True,
    with_reports: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
    ]
]:
    """Get Project

     Retrieve detailed information about a project by its ID.

    Args:
    - **id**: The ID of the project.
    - **with_sources**: Include sources in the response.
    - **with_reports**: Include reports in the response.

    Returns:
    - **ProjectWithSourcesDTO | ProjectWithReportsDTO | ProjectWithAllRelationsDTO |
    ProjectBaseSchema**: The detailed project information.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **401 Unauthorized (ProjectNotOwnedByUser)**: Raised if the project does not belong to the
    authenticated user.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.
        with_reports (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema]]
    """

    kwargs = _get_kwargs(
        id=id,
        with_sources=with_sources,
        with_reports=with_reports,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = True,
    with_reports: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
    ]
]:
    """Get Project

     Retrieve detailed information about a project by its ID.

    Args:
    - **id**: The ID of the project.
    - **with_sources**: Include sources in the response.
    - **with_reports**: Include reports in the response.

    Returns:
    - **ProjectWithSourcesDTO | ProjectWithReportsDTO | ProjectWithAllRelationsDTO |
    ProjectBaseSchema**: The detailed project information.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **401 Unauthorized (ProjectNotOwnedByUser)**: Raised if the project does not belong to the
    authenticated user.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.
        with_reports (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema]
    """

    return sync_detailed(
        id=id,
        client=client,
        with_sources=with_sources,
        with_reports=with_reports,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = True,
    with_reports: Union[Unset, bool] = True,
) -> Response[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
    ]
]:
    """Get Project

     Retrieve detailed information about a project by its ID.

    Args:
    - **id**: The ID of the project.
    - **with_sources**: Include sources in the response.
    - **with_reports**: Include reports in the response.

    Returns:
    - **ProjectWithSourcesDTO | ProjectWithReportsDTO | ProjectWithAllRelationsDTO |
    ProjectBaseSchema**: The detailed project information.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **401 Unauthorized (ProjectNotOwnedByUser)**: Raised if the project does not belong to the
    authenticated user.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.
        with_reports (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema]]
    """

    kwargs = _get_kwargs(
        id=id,
        with_sources=with_sources,
        with_reports=with_reports,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    with_sources: Union[Unset, bool] = True,
    with_reports: Union[Unset, bool] = True,
) -> Optional[
    Union[
        HTTPValidationError,
        ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema,
    ]
]:
    """Get Project

     Retrieve detailed information about a project by its ID.

    Args:
    - **id**: The ID of the project.
    - **with_sources**: Include sources in the response.
    - **with_reports**: Include reports in the response.

    Returns:
    - **ProjectWithSourcesDTO | ProjectWithReportsDTO | ProjectWithAllRelationsDTO |
    ProjectBaseSchema**: The detailed project information.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **401 Unauthorized (ProjectNotOwnedByUser)**: Raised if the project does not belong to the
    authenticated user.

    Args:
        id (UUID):
        with_sources (Union[Unset, bool]):  Default: True.
        with_reports (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUnionProjectWithSourcesDTOProjectWithReportsDTOProjectWithAllRelationsDTOProjectBaseSchema]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            with_sources=with_sources,
            with_reports=with_reports,
        )
    ).parsed
