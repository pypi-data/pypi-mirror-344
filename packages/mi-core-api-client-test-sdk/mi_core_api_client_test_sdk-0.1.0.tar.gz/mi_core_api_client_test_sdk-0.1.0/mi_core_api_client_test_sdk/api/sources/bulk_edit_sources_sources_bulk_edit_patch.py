from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_source_schema import ResponseWithMetadataSchemalistSourceSchema
from ...models.source_update_schema import SourceUpdateSchema
from ...types import Response


def _get_kwargs(
    *,
    body: SourceUpdateSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/sources/bulk-edit",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistSourceSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SourceUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Edit Sources

     Update a list of sources with new params field.

    This endpoint returns newly updated sources for user.

    Args:
    - **data[SourceUpdateSchema]**: object with list of source id's and new params.

    Returns:
    - **list[SourceSchema]**: A list of newly updated sources.

    Raises:
    - **400 Bad Request (Unsupported Document Type)**: Raised if the sources provided has different
    document types.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        body (SourceUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]
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
    body: SourceUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Edit Sources

     Update a list of sources with new params field.

    This endpoint returns newly updated sources for user.

    Args:
    - **data[SourceUpdateSchema]**: object with list of source id's and new params.

    Returns:
    - **list[SourceSchema]**: A list of newly updated sources.

    Raises:
    - **400 Bad Request (Unsupported Document Type)**: Raised if the sources provided has different
    document types.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        body (SourceUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SourceUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Edit Sources

     Update a list of sources with new params field.

    This endpoint returns newly updated sources for user.

    Args:
    - **data[SourceUpdateSchema]**: object with list of source id's and new params.

    Returns:
    - **list[SourceSchema]**: A list of newly updated sources.

    Raises:
    - **400 Bad Request (Unsupported Document Type)**: Raised if the sources provided has different
    document types.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        body (SourceUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SourceUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Edit Sources

     Update a list of sources with new params field.

    This endpoint returns newly updated sources for user.

    Args:
    - **data[SourceUpdateSchema]**: object with list of source id's and new params.

    Returns:
    - **list[SourceSchema]**: A list of newly updated sources.

    Raises:
    - **400 Bad Request (Unsupported Document Type)**: Raised if the sources provided has different
    document types.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        body (SourceUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
