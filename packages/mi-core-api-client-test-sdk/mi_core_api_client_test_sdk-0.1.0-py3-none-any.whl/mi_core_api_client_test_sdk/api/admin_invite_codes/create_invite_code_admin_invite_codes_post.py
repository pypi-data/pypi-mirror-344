from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.invite_code_schema import InviteCodeSchema
from ...models.response_with_metadata_schema_invite_code_schema import ResponseWithMetadataSchemaInviteCodeSchema
from ...types import Response


def _get_kwargs(
    *,
    body: InviteCodeSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/invite_codes",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaInviteCodeSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: InviteCodeSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]:
    """Create Invite Code

     Create a new invite code.

    This endpoint allows superusers to create a new invite code.

    Args:
    - **code[InviteCodeSchema]**: Schema containing the invite code to create.

    Returns:
    - **InviteCodeSchema**: The details of the newly created invite code.

    Raises:
    - **409 Conflict (InviteCodeAlreadyExist)**: Raised if an invite code with the same value already
    exists.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        body (InviteCodeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]
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
    body: InviteCodeSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]:
    """Create Invite Code

     Create a new invite code.

    This endpoint allows superusers to create a new invite code.

    Args:
    - **code[InviteCodeSchema]**: Schema containing the invite code to create.

    Returns:
    - **InviteCodeSchema**: The details of the newly created invite code.

    Raises:
    - **409 Conflict (InviteCodeAlreadyExist)**: Raised if an invite code with the same value already
    exists.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        body (InviteCodeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: InviteCodeSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]:
    """Create Invite Code

     Create a new invite code.

    This endpoint allows superusers to create a new invite code.

    Args:
    - **code[InviteCodeSchema]**: Schema containing the invite code to create.

    Returns:
    - **InviteCodeSchema**: The details of the newly created invite code.

    Raises:
    - **409 Conflict (InviteCodeAlreadyExist)**: Raised if an invite code with the same value already
    exists.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        body (InviteCodeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: InviteCodeSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]]:
    """Create Invite Code

     Create a new invite code.

    This endpoint allows superusers to create a new invite code.

    Args:
    - **code[InviteCodeSchema]**: Schema containing the invite code to create.

    Returns:
    - **InviteCodeSchema**: The details of the newly created invite code.

    Raises:
    - **409 Conflict (InviteCodeAlreadyExist)**: Raised if an invite code with the same value already
    exists.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Args:
        body (InviteCodeSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaInviteCodeSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
