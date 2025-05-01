from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_with_metadata_schema_union_user_info_schema_api_key_dto import (
    ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user/me",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]:
    """Get Current User Func

     Get current user

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]:
    """Get Current User Func

     Get current user

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]:
    """Get Current User Func

     Get current user

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO]:
    """Get Current User Func

     Get current user

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemaUnionUserInfoSchemaAPIKeyDTO
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
