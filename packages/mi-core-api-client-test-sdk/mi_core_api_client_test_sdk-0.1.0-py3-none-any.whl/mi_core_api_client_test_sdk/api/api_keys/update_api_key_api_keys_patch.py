from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_key_upgrade_schema import APIKeyUpgradeSchema
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_api_key_dto import ResponseWithMetadataSchemaAPIKeyDTO
from ...types import Response


def _get_kwargs(
    *,
    body: APIKeyUpgradeSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api-keys",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaAPIKeyDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: APIKeyUpgradeSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Update Api Key

     Update the API key details for the authenticated user.

    This endpoint allows users to update the name or expiration date of their API key.

    Args:
    - **data[APIKeyUpgradeSchema]**: Schema for updating the API key.

    Returns:
    - **APIKeyDTO**: The updated API key details.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the user does not have an API key.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not authenticated.

    Args:
        body (APIKeyUpgradeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]
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
    body: APIKeyUpgradeSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Update Api Key

     Update the API key details for the authenticated user.

    This endpoint allows users to update the name or expiration date of their API key.

    Args:
    - **data[APIKeyUpgradeSchema]**: Schema for updating the API key.

    Returns:
    - **APIKeyDTO**: The updated API key details.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the user does not have an API key.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not authenticated.

    Args:
        body (APIKeyUpgradeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: APIKeyUpgradeSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Update Api Key

     Update the API key details for the authenticated user.

    This endpoint allows users to update the name or expiration date of their API key.

    Args:
    - **data[APIKeyUpgradeSchema]**: Schema for updating the API key.

    Returns:
    - **APIKeyDTO**: The updated API key details.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the user does not have an API key.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not authenticated.

    Args:
        body (APIKeyUpgradeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: APIKeyUpgradeSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]]:
    """Update Api Key

     Update the API key details for the authenticated user.

    This endpoint allows users to update the name or expiration date of their API key.

    Args:
    - **data[APIKeyUpgradeSchema]**: Schema for updating the API key.

    Returns:
    - **APIKeyDTO**: The updated API key details.

    Raises:
    - **404 Not Found (APIKeyNotFound)**: Raised if the user does not have an API key.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not authenticated.

    Args:
        body (APIKeyUpgradeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaAPIKeyDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
