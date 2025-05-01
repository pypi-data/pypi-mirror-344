from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_with_metadata_schemalist_api_key_dto import ResponseWithMetadataSchemalistAPIKeyDTO
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/api-keys",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResponseWithMetadataSchemalistAPIKeyDTO]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistAPIKeyDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResponseWithMetadataSchemalistAPIKeyDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemalistAPIKeyDTO]:
    """Get All Api Keys

     Retrieve all API keys.

    This endpoint allows superusers to fetch a list of all API keys in the system.

    Returns:
    - **list[APIKeyDTO]**: A list of all API keys in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemalistAPIKeyDTO]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemalistAPIKeyDTO]:
    """Get All Api Keys

     Retrieve all API keys.

    This endpoint allows superusers to fetch a list of all API keys in the system.

    Returns:
    - **list[APIKeyDTO]**: A list of all API keys in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemalistAPIKeyDTO
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemalistAPIKeyDTO]:
    """Get All Api Keys

     Retrieve all API keys.

    This endpoint allows superusers to fetch a list of all API keys in the system.

    Returns:
    - **list[APIKeyDTO]**: A list of all API keys in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemalistAPIKeyDTO]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemalistAPIKeyDTO]:
    """Get All Api Keys

     Retrieve all API keys.

    This endpoint allows superusers to fetch a list of all API keys in the system.

    Returns:
    - **list[APIKeyDTO]**: A list of all API keys in the system.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemalistAPIKeyDTO
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
