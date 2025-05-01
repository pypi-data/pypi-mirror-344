from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_update_schema import ProjectUpdateSchema
from ...models.response_with_metadata_schema_project_base_schema import ResponseWithMetadataSchemaProjectBaseSchema
from ...types import Response


def _get_kwargs(
    id: UUID,
    *,
    body: ProjectUpdateSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/projects/{id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaProjectBaseSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
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
    body: ProjectUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Update Project

     Update a project by its ID for the authenticated user.

    Args:
    - **id**: The ID of the project to update.
    - **data[ProjectUpdateSchema]**: Schema containing the updated project details.

    Returns:
    - **ProjectBaseSchema**: The updated project details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found**: Raised if the project does not exist or is inaccessible by the user.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.

    Args:
        id (UUID):
        body (ProjectUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]
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
    body: ProjectUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Update Project

     Update a project by its ID for the authenticated user.

    Args:
    - **id**: The ID of the project to update.
    - **data[ProjectUpdateSchema]**: Schema containing the updated project details.

    Returns:
    - **ProjectBaseSchema**: The updated project details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found**: Raised if the project does not exist or is inaccessible by the user.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.

    Args:
        id (UUID):
        body (ProjectUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]
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
    body: ProjectUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Update Project

     Update a project by its ID for the authenticated user.

    Args:
    - **id**: The ID of the project to update.
    - **data[ProjectUpdateSchema]**: Schema containing the updated project details.

    Returns:
    - **ProjectBaseSchema**: The updated project details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found**: Raised if the project does not exist or is inaccessible by the user.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.

    Args:
        id (UUID):
        body (ProjectUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]
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
    body: ProjectUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Update Project

     Update a project by its ID for the authenticated user.

    Args:
    - **id**: The ID of the project to update.
    - **data[ProjectUpdateSchema]**: Schema containing the updated project details.

    Returns:
    - **ProjectBaseSchema**: The updated project details.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **404 Not Found**: Raised if the project does not exist or is inaccessible by the user.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.

    Args:
        id (UUID):
        body (ProjectUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
