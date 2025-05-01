from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_with_all_relations_and_workflows_dto import ProjectWithAllRelationsAndWorkflowsDTO
from ...types import UNSET, Response


def _get_kwargs(
    id: UUID,
    *,
    new_project_name: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["new_project_name"] = new_project_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/templates/{id}/import",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]:
    if response.status_code == 201:
        response_201 = ProjectWithAllRelationsAndWorkflowsDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]:
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
    new_project_name: str,
) -> Response[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]:
    """Import Project From Template

     Create a new project by importing configuration from a template.

    Args:
    - **id**: UUID of the template to use.
    - **new_project_name**: Name to assign to the new project.

    Returns:
    - **ProjectWithAllRelationsAndWorkflowsDTO**: New project created using the template.

    Raises:
    - **400 Bad Request (InvalidProjectInSourceImport)**: Raised if the template includes references to
    projects the user does not own.
    - **400 Bad Request (InvalidWorkflowImport)**: Raised if the workflow references entities (e.g.
    reports, custom fields) that are not included in the import.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (TemplateNotFoundException)**: Raised if no template is found based on the
    provided ID.
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.
    - **409 Conflict (ProjectAlreadyExistsException)**: Raised if a project with the same name already
    exists for this user.

    Args:
        id (UUID):
        new_project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]
    """

    kwargs = _get_kwargs(
        id=id,
        new_project_name=new_project_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    new_project_name: str,
) -> Optional[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]:
    """Import Project From Template

     Create a new project by importing configuration from a template.

    Args:
    - **id**: UUID of the template to use.
    - **new_project_name**: Name to assign to the new project.

    Returns:
    - **ProjectWithAllRelationsAndWorkflowsDTO**: New project created using the template.

    Raises:
    - **400 Bad Request (InvalidProjectInSourceImport)**: Raised if the template includes references to
    projects the user does not own.
    - **400 Bad Request (InvalidWorkflowImport)**: Raised if the workflow references entities (e.g.
    reports, custom fields) that are not included in the import.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (TemplateNotFoundException)**: Raised if no template is found based on the
    provided ID.
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.
    - **409 Conflict (ProjectAlreadyExistsException)**: Raised if a project with the same name already
    exists for this user.

    Args:
        id (UUID):
        new_project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]
    """

    return sync_detailed(
        id=id,
        client=client,
        new_project_name=new_project_name,
    ).parsed


async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    new_project_name: str,
) -> Response[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]:
    """Import Project From Template

     Create a new project by importing configuration from a template.

    Args:
    - **id**: UUID of the template to use.
    - **new_project_name**: Name to assign to the new project.

    Returns:
    - **ProjectWithAllRelationsAndWorkflowsDTO**: New project created using the template.

    Raises:
    - **400 Bad Request (InvalidProjectInSourceImport)**: Raised if the template includes references to
    projects the user does not own.
    - **400 Bad Request (InvalidWorkflowImport)**: Raised if the workflow references entities (e.g.
    reports, custom fields) that are not included in the import.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (TemplateNotFoundException)**: Raised if no template is found based on the
    provided ID.
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.
    - **409 Conflict (ProjectAlreadyExistsException)**: Raised if a project with the same name already
    exists for this user.

    Args:
        id (UUID):
        new_project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]
    """

    kwargs = _get_kwargs(
        id=id,
        new_project_name=new_project_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    new_project_name: str,
) -> Optional[Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]]:
    """Import Project From Template

     Create a new project by importing configuration from a template.

    Args:
    - **id**: UUID of the template to use.
    - **new_project_name**: Name to assign to the new project.

    Returns:
    - **ProjectWithAllRelationsAndWorkflowsDTO**: New project created using the template.

    Raises:
    - **400 Bad Request (InvalidProjectInSourceImport)**: Raised if the template includes references to
    projects the user does not own.
    - **400 Bad Request (InvalidWorkflowImport)**: Raised if the workflow references entities (e.g.
    reports, custom fields) that are not included in the import.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (TemplateNotFoundException)**: Raised if no template is found based on the
    provided ID.
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.
    - **409 Conflict (ProjectAlreadyExistsException)**: Raised if a project with the same name already
    exists for this user.

    Args:
        id (UUID):
        new_project_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectWithAllRelationsAndWorkflowsDTO]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            new_project_name=new_project_name,
        )
    ).parsed
