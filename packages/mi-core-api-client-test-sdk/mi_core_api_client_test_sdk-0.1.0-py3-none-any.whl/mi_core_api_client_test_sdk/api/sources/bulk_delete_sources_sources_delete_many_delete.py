from http import HTTPStatus
from typing import Any, Optional, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_source_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(source_ids, Unset):
        json_source_ids = []
        for source_ids_item_data in source_ids:
            source_ids_item = str(source_ids_item_data)
            json_source_ids.append(source_ids_item)

    params["source_ids"] = json_source_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/sources/delete-many",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Bulk Delete Sources

     Delete a list of sources.

    This endpoint deletes a list of sources for the user by provided ids.

    Args:
    - **source_ids**: List of source ids to delete.

    Returns:
    - **204 No Content**: A successful response with no content.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        source_ids (Union[Unset, list[UUID]]): List of source Ids to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        source_ids=source_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Bulk Delete Sources

     Delete a list of sources.

    This endpoint deletes a list of sources for the user by provided ids.

    Args:
    - **source_ids**: List of source ids to delete.

    Returns:
    - **204 No Content**: A successful response with no content.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        source_ids (Union[Unset, list[UUID]]): List of source Ids to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        source_ids=source_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Bulk Delete Sources

     Delete a list of sources.

    This endpoint deletes a list of sources for the user by provided ids.

    Args:
    - **source_ids**: List of source ids to delete.

    Returns:
    - **204 No Content**: A successful response with no content.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        source_ids (Union[Unset, list[UUID]]): List of source Ids to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        source_ids=source_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Bulk Delete Sources

     Delete a list of sources.

    This endpoint deletes a list of sources for the user by provided ids.

    Args:
    - **source_ids**: List of source ids to delete.

    Returns:
    - **204 No Content**: A successful response with no content.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        source_ids (Union[Unset, list[UUID]]): List of source Ids to delete sources from

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            source_ids=source_ids,
        )
    ).parsed
