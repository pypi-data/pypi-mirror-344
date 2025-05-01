from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_collection_schema import ResponseWithMetadataSchemaCollectionSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection_name: str,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["collection_name"] = collection_name

    json_source_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(source_ids, Unset):
        json_source_ids = []
        for source_ids_item_data in source_ids:
            source_ids_item = str(source_ids_item_data)
            json_source_ids.append(source_ids_item)

    params["source_ids"] = json_source_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/collections",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]:
    if response.status_code == 201:
        response_201 = ResponseWithMetadataSchemaCollectionSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]:
    """Create Collection

     Create a new collection for the signed-in user.

    This endpoint creates a new collection for the signed-in user.

    Args:
    - **collection_name**: The name of the collection to create.

    Returns:
    - **CollectionSchema**: A schema containing information about the created collection.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (str):
        source_ids (Union[Unset, list[UUID]]): List of source IDs to attach to collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        source_ids=source_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]:
    """Create Collection

     Create a new collection for the signed-in user.

    This endpoint creates a new collection for the signed-in user.

    Args:
    - **collection_name**: The name of the collection to create.

    Returns:
    - **CollectionSchema**: A schema containing information about the created collection.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (str):
        source_ids (Union[Unset, list[UUID]]): List of source IDs to attach to collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]
    """

    return sync_detailed(
        client=client,
        collection_name=collection_name,
        source_ids=source_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]:
    """Create Collection

     Create a new collection for the signed-in user.

    This endpoint creates a new collection for the signed-in user.

    Args:
    - **collection_name**: The name of the collection to create.

    Returns:
    - **CollectionSchema**: A schema containing information about the created collection.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (str):
        source_ids (Union[Unset, list[UUID]]): List of source IDs to attach to collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        source_ids=source_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    source_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]]:
    """Create Collection

     Create a new collection for the signed-in user.

    This endpoint creates a new collection for the signed-in user.

    Args:
    - **collection_name**: The name of the collection to create.

    Returns:
    - **CollectionSchema**: A schema containing information about the created collection.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the provided links and source_type are not
    the same.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.

    Args:
        collection_name (str):
        source_ids (Union[Unset, list[UUID]]): List of source IDs to attach to collection

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaCollectionSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_name=collection_name,
            source_ids=source_ids,
        )
    ).parsed
