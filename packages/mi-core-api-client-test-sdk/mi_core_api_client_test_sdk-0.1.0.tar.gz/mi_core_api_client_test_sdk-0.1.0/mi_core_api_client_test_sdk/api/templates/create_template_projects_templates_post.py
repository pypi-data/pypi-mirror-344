from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_template_schema import CreateTemplateSchema
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_template_dto import ResponseWithMetadataSchemaTemplateDTO
from ...types import Response


def _get_kwargs(
    *,
    body: CreateTemplateSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/templates",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]:
    if response.status_code == 201:
        response_201 = ResponseWithMetadataSchemaTemplateDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateTemplateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]:
    """Create Template

     Create a new template from an existing project configuration.

    Args:
    - **template**: Schema describing the template content and included components.

    Returns:
    - **TemplateDTO**: A schema containing basic info about the created template.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.

    Args:
        body (CreateTemplateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]
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
    body: CreateTemplateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]:
    """Create Template

     Create a new template from an existing project configuration.

    Args:
    - **template**: Schema describing the template content and included components.

    Returns:
    - **TemplateDTO**: A schema containing basic info about the created template.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.

    Args:
        body (CreateTemplateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateTemplateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]:
    """Create Template

     Create a new template from an existing project configuration.

    Args:
    - **template**: Schema describing the template content and included components.

    Returns:
    - **TemplateDTO**: A schema containing basic info about the created template.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.

    Args:
        body (CreateTemplateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateTemplateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]]:
    """Create Template

     Create a new template from an existing project configuration.

    Args:
    - **template**: Schema describing the template content and included components.

    Returns:
    - **TemplateDTO**: A schema containing basic info about the created template.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.

    Args:
        body (CreateTemplateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
