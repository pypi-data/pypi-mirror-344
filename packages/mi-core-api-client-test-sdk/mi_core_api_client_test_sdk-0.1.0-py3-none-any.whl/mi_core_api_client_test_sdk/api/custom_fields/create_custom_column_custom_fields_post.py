from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_custom_column_apply_prompt import CreateCustomColumnApplyPrompt
from ...models.create_custom_column_data_lookup import CreateCustomColumnDataLookup
from ...models.create_custom_column_validated_prompt import CreateCustomColumnValidatedPrompt
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_custom_column_base_schema import (
    ResponseWithMetadataSchemaCustomColumnBaseSchema,
)
from ...types import Response


def _get_kwargs(
    *,
    body: Union["CreateCustomColumnApplyPrompt", "CreateCustomColumnDataLookup", "CreateCustomColumnValidatedPrompt"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/custom-fields",
    }

    _body: dict[str, Any]
    if isinstance(body, CreateCustomColumnDataLookup):
        _body = body.to_dict()
    elif isinstance(body, CreateCustomColumnApplyPrompt):
        _body = body.to_dict()
    else:
        _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]:
    if response.status_code == 201:
        response_201 = ResponseWithMetadataSchemaCustomColumnBaseSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union["CreateCustomColumnApplyPrompt", "CreateCustomColumnDataLookup", "CreateCustomColumnValidatedPrompt"],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]:
    """Create Custom Column

     Create a new custom field column for the signed-in user's project.

    Args:
    - **input_data**: Configuration of the custom column to be created depending on the required type in
    next formats:
        - CreateCustomColumnDataLookup
        - CreateCustomColumnApplyPrompt
        - CreateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnBaseSchema**: A schema containing information about the created custom field column.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        body (Union['CreateCustomColumnApplyPrompt', 'CreateCustomColumnDataLookup',
            'CreateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]
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
    body: Union["CreateCustomColumnApplyPrompt", "CreateCustomColumnDataLookup", "CreateCustomColumnValidatedPrompt"],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]:
    """Create Custom Column

     Create a new custom field column for the signed-in user's project.

    Args:
    - **input_data**: Configuration of the custom column to be created depending on the required type in
    next formats:
        - CreateCustomColumnDataLookup
        - CreateCustomColumnApplyPrompt
        - CreateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnBaseSchema**: A schema containing information about the created custom field column.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        body (Union['CreateCustomColumnApplyPrompt', 'CreateCustomColumnDataLookup',
            'CreateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union["CreateCustomColumnApplyPrompt", "CreateCustomColumnDataLookup", "CreateCustomColumnValidatedPrompt"],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]:
    """Create Custom Column

     Create a new custom field column for the signed-in user's project.

    Args:
    - **input_data**: Configuration of the custom column to be created depending on the required type in
    next formats:
        - CreateCustomColumnDataLookup
        - CreateCustomColumnApplyPrompt
        - CreateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnBaseSchema**: A schema containing information about the created custom field column.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        body (Union['CreateCustomColumnApplyPrompt', 'CreateCustomColumnDataLookup',
            'CreateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union["CreateCustomColumnApplyPrompt", "CreateCustomColumnDataLookup", "CreateCustomColumnValidatedPrompt"],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]]:
    """Create Custom Column

     Create a new custom field column for the signed-in user's project.

    Args:
    - **input_data**: Configuration of the custom column to be created depending on the required type in
    next formats:
        - CreateCustomColumnDataLookup
        - CreateCustomColumnApplyPrompt
        - CreateCustomColumnValidatedPrompt

    Returns:
    - **CustomColumnBaseSchema**: A schema containing information about the created custom field column.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        body (Union['CreateCustomColumnApplyPrompt', 'CreateCustomColumnDataLookup',
            'CreateCustomColumnValidatedPrompt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCustomColumnBaseSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
