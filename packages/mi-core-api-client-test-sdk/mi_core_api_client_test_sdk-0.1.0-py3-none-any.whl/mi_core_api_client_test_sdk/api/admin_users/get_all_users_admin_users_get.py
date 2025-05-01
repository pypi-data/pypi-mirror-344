from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_with_metadata_schemalist_user_schema import ResponseWithMetadataSchemalistUserSchema
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/users",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResponseWithMetadataSchemalistUserSchema]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUserSchema.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResponseWithMetadataSchemalistUserSchema]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemalistUserSchema]:
    """Get All Users

     Retrieve all users in the system.

    This endpoint allows superusers to fetch a list of all registered users.

    Returns:
    - **list[UserSchema]**: A list of all users in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemalistUserSchema]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemalistUserSchema]:
    """Get All Users

     Retrieve all users in the system.

    This endpoint allows superusers to fetch a list of all registered users.

    Returns:
    - **list[UserSchema]**: A list of all users in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemalistUserSchema
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemalistUserSchema]:
    """Get All Users

     Retrieve all users in the system.

    This endpoint allows superusers to fetch a list of all registered users.

    Returns:
    - **list[UserSchema]**: A list of all users in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemalistUserSchema]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemalistUserSchema]:
    """Get All Users

     Retrieve all users in the system.

    This endpoint allows superusers to fetch a list of all registered users.

    Returns:
    - **list[UserSchema]**: A list of all users in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemalistUserSchema
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
