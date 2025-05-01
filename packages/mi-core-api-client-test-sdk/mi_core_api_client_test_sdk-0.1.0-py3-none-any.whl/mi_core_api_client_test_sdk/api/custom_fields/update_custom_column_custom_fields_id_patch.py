from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_custom_column_dto import ResponseWithMetadataSchemaCustomColumnDTO
from ...models.update_custom_column_apply_prompt import UpdateCustomColumnApplyPrompt
from ...models.update_custom_column_data_lookup import UpdateCustomColumnDataLookup
from ...models.update_custom_column_validated_prompt import UpdateCustomColumnValidatedPrompt
from ...types import Response


def _get_kwargs(
    id: UUID,
    *,
    body: Union["UpdateCustomColumnApplyPrompt", "UpdateCustomColumnDataLookup", "UpdateCustomColumnValidatedPrompt"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/custom-fields/{id}",
    }

    _body: dict[str, Any]
    if isinstance(body, UpdateCustomColumnDataLookup):
        _body = body.to_dict()
    elif isinstance(body, UpdateCustomColumnApplyPrompt):
        _body = body.to_dict()
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaCustomColumnDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]:
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
    body: Union["UpdateCustomColumnApplyPrompt", "UpdateCustomColumnDataLookup", "UpdateCustomColumnValidatedPrompt"],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]:
    """Update Custom Column

     Update configurations of a custom field column for the signed-in user's project.

    Args:
    - **id**: ID of the custom column to be updated.
    - **input_data**: Configuration of the custom column to be updated depending on the required type in
    next formats:
        - UpdateCustomColumnDataLookup
        - UpdateCustomColumnApplyPrompt
        - UpdateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnDTO**: A schema containing information about the updated custom field column.

    Raises:
    - **400 Bad Request (InvalidCustomFieldUpdateValue)**: Raised if required fields for the new column
    type are missing.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        id (UUID):
        body (Union['UpdateCustomColumnApplyPrompt', 'UpdateCustomColumnDataLookup',
            'UpdateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]
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
    body: Union["UpdateCustomColumnApplyPrompt", "UpdateCustomColumnDataLookup", "UpdateCustomColumnValidatedPrompt"],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]:
    """Update Custom Column

     Update configurations of a custom field column for the signed-in user's project.

    Args:
    - **id**: ID of the custom column to be updated.
    - **input_data**: Configuration of the custom column to be updated depending on the required type in
    next formats:
        - UpdateCustomColumnDataLookup
        - UpdateCustomColumnApplyPrompt
        - UpdateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnDTO**: A schema containing information about the updated custom field column.

    Raises:
    - **400 Bad Request (InvalidCustomFieldUpdateValue)**: Raised if required fields for the new column
    type are missing.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        id (UUID):
        body (Union['UpdateCustomColumnApplyPrompt', 'UpdateCustomColumnDataLookup',
            'UpdateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]
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
    body: Union["UpdateCustomColumnApplyPrompt", "UpdateCustomColumnDataLookup", "UpdateCustomColumnValidatedPrompt"],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]:
    """Update Custom Column

     Update configurations of a custom field column for the signed-in user's project.

    Args:
    - **id**: ID of the custom column to be updated.
    - **input_data**: Configuration of the custom column to be updated depending on the required type in
    next formats:
        - UpdateCustomColumnDataLookup
        - UpdateCustomColumnApplyPrompt
        - UpdateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnDTO**: A schema containing information about the updated custom field column.

    Raises:
    - **400 Bad Request (InvalidCustomFieldUpdateValue)**: Raised if required fields for the new column
    type are missing.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        id (UUID):
        body (Union['UpdateCustomColumnApplyPrompt', 'UpdateCustomColumnDataLookup',
            'UpdateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]
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
    body: Union["UpdateCustomColumnApplyPrompt", "UpdateCustomColumnDataLookup", "UpdateCustomColumnValidatedPrompt"],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]]:
    """Update Custom Column

     Update configurations of a custom field column for the signed-in user's project.

    Args:
    - **id**: ID of the custom column to be updated.
    - **input_data**: Configuration of the custom column to be updated depending on the required type in
    next formats:
        - UpdateCustomColumnDataLookup
        - UpdateCustomColumnApplyPrompt
        - UpdateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnDTO**: A schema containing information about the updated custom field column.

    Raises:
    - **400 Bad Request (InvalidCustomFieldUpdateValue)**: Raised if required fields for the new column
    type are missing.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        id (UUID):
        body (Union['UpdateCustomColumnApplyPrompt', 'UpdateCustomColumnDataLookup',
            'UpdateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnDTO]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
