from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_import_template_projects_templates_import_post import BodyImportTemplateProjectsTemplatesImportPost
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_template_detailed_dto import ResponseWithMetadataSchemaTemplateDetailedDTO
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: BodyImportTemplateProjectsTemplatesImportPost,
    template_name: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["template_name"] = template_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/templates/import",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaTemplateDetailedDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyImportTemplateProjectsTemplatesImportPost,
    template_name: str,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]:
    """Import Template

     Import a template from a JSON file.

    Args:
    - **template_name**: Name to assign to the imported template.
    - **template_file**: JSON file with valid template structure.

    Returns:
    - **TemplateDetailedDTO**: Detailed representation of the imported template.

    Raises:
    - **400 Bad Request (InvalidParamInTemplateImport)**: Raised if the provided template structure is
    invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **409 Conflict (TemplateAlreadyExistsException)**: Raised if a template with the same name already
    exists for this user.
    - **422 Unprocessable Entity (ValueError)**: Raised if the uploaded file is not valid JSON or does
    not match the expected schema.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during provided
    file parsing.

    Args:
        template_name (str):
        body (BodyImportTemplateProjectsTemplatesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]
    """

    kwargs = _get_kwargs(
        body=body,
        template_name=template_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: BodyImportTemplateProjectsTemplatesImportPost,
    template_name: str,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]:
    """Import Template

     Import a template from a JSON file.

    Args:
    - **template_name**: Name to assign to the imported template.
    - **template_file**: JSON file with valid template structure.

    Returns:
    - **TemplateDetailedDTO**: Detailed representation of the imported template.

    Raises:
    - **400 Bad Request (InvalidParamInTemplateImport)**: Raised if the provided template structure is
    invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **409 Conflict (TemplateAlreadyExistsException)**: Raised if a template with the same name already
    exists for this user.
    - **422 Unprocessable Entity (ValueError)**: Raised if the uploaded file is not valid JSON or does
    not match the expected schema.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during provided
    file parsing.

    Args:
        template_name (str):
        body (BodyImportTemplateProjectsTemplatesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]
    """

    return sync_detailed(
        client=client,
        body=body,
        template_name=template_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyImportTemplateProjectsTemplatesImportPost,
    template_name: str,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]:
    """Import Template

     Import a template from a JSON file.

    Args:
    - **template_name**: Name to assign to the imported template.
    - **template_file**: JSON file with valid template structure.

    Returns:
    - **TemplateDetailedDTO**: Detailed representation of the imported template.

    Raises:
    - **400 Bad Request (InvalidParamInTemplateImport)**: Raised if the provided template structure is
    invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **409 Conflict (TemplateAlreadyExistsException)**: Raised if a template with the same name already
    exists for this user.
    - **422 Unprocessable Entity (ValueError)**: Raised if the uploaded file is not valid JSON or does
    not match the expected schema.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during provided
    file parsing.

    Args:
        template_name (str):
        body (BodyImportTemplateProjectsTemplatesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]
    """

    kwargs = _get_kwargs(
        body=body,
        template_name=template_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BodyImportTemplateProjectsTemplatesImportPost,
    template_name: str,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]]:
    """Import Template

     Import a template from a JSON file.

    Args:
    - **template_name**: Name to assign to the imported template.
    - **template_file**: JSON file with valid template structure.

    Returns:
    - **TemplateDetailedDTO**: Detailed representation of the imported template.

    Raises:
    - **400 Bad Request (InvalidParamInTemplateImport)**: Raised if the provided template structure is
    invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **409 Conflict (TemplateAlreadyExistsException)**: Raised if a template with the same name already
    exists for this user.
    - **422 Unprocessable Entity (ValueError)**: Raised if the uploaded file is not valid JSON or does
    not match the expected schema.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during provided
    file parsing.

    Args:
        template_name (str):
        body (BodyImportTemplateProjectsTemplatesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaTemplateDetailedDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            template_name=template_name,
        )
    ).parsed
