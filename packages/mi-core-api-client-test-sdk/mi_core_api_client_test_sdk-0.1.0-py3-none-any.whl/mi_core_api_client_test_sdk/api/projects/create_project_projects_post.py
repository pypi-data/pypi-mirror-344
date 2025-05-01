from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_create_request_schema import ProjectCreateRequestSchema
from ...models.response_with_metadata_schema_project_base_schema import ResponseWithMetadataSchemaProjectBaseSchema
from ...types import Response


def _get_kwargs(
    *,
    body: ProjectCreateRequestSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    if response.status_code == 201:
        response_201 = ResponseWithMetadataSchemaProjectBaseSchema.from_dict(response.json())

        return response_201
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
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequestSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Create Project

     Create a new project for the authenticated user.

    Args:
    - **request[ProjectCreateRequestSchema]**: Schema containing the new project details.

    Returns:
    - **ProjectBaseSchema**: The details of the newly created project.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided project details are invalid.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.
    - **404 Not Found (ProjectBadCollectionsProvided)**: Raised if the provided collection IDs are not
    found.
    - **404 Not Found (ProjectBadSourcesProvided)**: Raised if the provided source IDs are not found.
    - **404 Not Found (ProjectEmptyException)**: Raised if on the relation creation some ids where
    corrupted.

    Args:
        body (ProjectCreateRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequestSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Create Project

     Create a new project for the authenticated user.

    Args:
    - **request[ProjectCreateRequestSchema]**: Schema containing the new project details.

    Returns:
    - **ProjectBaseSchema**: The details of the newly created project.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided project details are invalid.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.
    - **404 Not Found (ProjectBadCollectionsProvided)**: Raised if the provided collection IDs are not
    found.
    - **404 Not Found (ProjectBadSourcesProvided)**: Raised if the provided source IDs are not found.
    - **404 Not Found (ProjectEmptyException)**: Raised if on the relation creation some ids where
    corrupted.

    Args:
        body (ProjectCreateRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequestSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Create Project

     Create a new project for the authenticated user.

    Args:
    - **request[ProjectCreateRequestSchema]**: Schema containing the new project details.

    Returns:
    - **ProjectBaseSchema**: The details of the newly created project.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided project details are invalid.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.
    - **404 Not Found (ProjectBadCollectionsProvided)**: Raised if the provided collection IDs are not
    found.
    - **404 Not Found (ProjectBadSourcesProvided)**: Raised if the provided source IDs are not found.
    - **404 Not Found (ProjectEmptyException)**: Raised if on the relation creation some ids where
    corrupted.

    Args:
        body (ProjectCreateRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProjectCreateRequestSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]]:
    """Create Project

     Create a new project for the authenticated user.

    Args:
    - **request[ProjectCreateRequestSchema]**: Schema containing the new project details.

    Returns:
    - **ProjectBaseSchema**: The details of the newly created project.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **400 Bad Request**: Raised if the provided project details are invalid.
    - **409 Conflict (ProjectAlreadyExists)**: Raised if a project with the same name already exists for
    the user.
    - **404 Not Found (ProjectBadCollectionsProvided)**: Raised if the provided collection IDs are not
    found.
    - **404 Not Found (ProjectBadSourcesProvided)**: Raised if the provided source IDs are not found.
    - **404 Not Found (ProjectEmptyException)**: Raised if on the relation creation some ids where
    corrupted.

    Args:
        body (ProjectCreateRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaProjectBaseSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
