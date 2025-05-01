from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_uuid import ResponseWithMetadataSchemaUUID
from ...types import UNSET, Response


def _get_kwargs(
    *,
    id: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_id = str(id)
    params["id"] = json_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/analyze",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaUUID.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: UUID,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]:
    """Get Entities

     Analyze collection based on the running collection for the signed in user.

    This endpoint creates a background task to generate graph based on the sources in collection

    Args:
    - **id**: UUID of the running collection to run

    Returns:
    - **200 OK**: Started a generation in the background

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **500 Internal Server Error (MIGraphException)**: Raised if something went wrong on the MIGraph
    side

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id: UUID,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]:
    """Get Entities

     Analyze collection based on the running collection for the signed in user.

    This endpoint creates a background task to generate graph based on the sources in collection

    Args:
    - **id**: UUID of the running collection to run

    Returns:
    - **200 OK**: Started a generation in the background

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **500 Internal Server Error (MIGraphException)**: Raised if something went wrong on the MIGraph
    side

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]
    """

    return sync_detailed(
        client=client,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: UUID,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]:
    """Get Entities

     Analyze collection based on the running collection for the signed in user.

    This endpoint creates a background task to generate graph based on the sources in collection

    Args:
    - **id**: UUID of the running collection to run

    Returns:
    - **200 OK**: Started a generation in the background

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **500 Internal Server Error (MIGraphException)**: Raised if something went wrong on the MIGraph
    side

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id: UUID,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]]:
    """Get Entities

     Analyze collection based on the running collection for the signed in user.

    This endpoint creates a background task to generate graph based on the sources in collection

    Args:
    - **id**: UUID of the running collection to run

    Returns:
    - **200 OK**: Started a generation in the background

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **500 Internal Server Error (MIGraphException)**: Raised if something went wrong on the MIGraph
    side

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaUUID]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
        )
    ).parsed
