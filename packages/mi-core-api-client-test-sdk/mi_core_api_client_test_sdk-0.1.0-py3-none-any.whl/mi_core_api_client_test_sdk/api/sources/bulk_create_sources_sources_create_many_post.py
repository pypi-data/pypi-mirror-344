from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_source_schema import ResponseWithMetadataSchemalistSourceSchema
from ...models.source_create_many_schema import SourceCreateManySchema
from ...types import Response


def _get_kwargs(
    *,
    body: SourceCreateManySchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sources/create-many",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    if response.status_code == 201:
        response_201 = ResponseWithMetadataSchemalistSourceSchema.from_dict(response.json())

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
    body: SourceCreateManySchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Create Sources

     Creates multiple sources for the user.

    This endpoint returns list of newly created sources for user.

    Args:
    - **data[SourceCreateManySchema]**: object with list of source id's, source_type and source params.

    Returns:
    - **list[SourceSchema]**: A list of newly created sources.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        body (SourceCreateManySchema):

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
    body: SourceCreateManySchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Create Sources

     Creates multiple sources for the user.

    This endpoint returns list of newly created sources for user.

    Args:
    - **data[SourceCreateManySchema]**: object with list of source id's, source_type and source params.

    Returns:
    - **list[SourceSchema]**: A list of newly created sources.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        body (SourceCreateManySchema):

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
    body: SourceCreateManySchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Create Sources

     Creates multiple sources for the user.

    This endpoint returns list of newly created sources for user.

    Args:
    - **data[SourceCreateManySchema]**: object with list of source id's, source_type and source params.

    Returns:
    - **list[SourceSchema]**: A list of newly created sources.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        body (SourceCreateManySchema):

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
    body: SourceCreateManySchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistSourceSchema]]:
    """Bulk Create Sources

     Creates multiple sources for the user.

    This endpoint returns list of newly created sources for user.

    Args:
    - **data[SourceCreateManySchema]**: object with list of source id's, source_type and source params.

    Returns:
    - **list[SourceSchema]**: A list of newly created sources.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        body (SourceCreateManySchema):

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
