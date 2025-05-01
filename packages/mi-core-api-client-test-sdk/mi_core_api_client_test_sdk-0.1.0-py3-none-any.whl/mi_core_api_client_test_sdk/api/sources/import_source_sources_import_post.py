from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_import_source_sources_import_post import BodyImportSourceSourcesImportPost
from ...models.http_validation_error import HTTPValidationError
from ...models.source_schema import SourceSchema
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyImportSourceSourcesImportPost,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
    project_ids: Union[Unset, list[UUID]] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_collection_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(collection_ids, Unset):
        json_collection_ids = []
        for collection_ids_item_data in collection_ids:
            collection_ids_item = str(collection_ids_item_data)
            json_collection_ids.append(collection_ids_item)

    params["collection_ids"] = json_collection_ids

    json_project_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(project_ids, Unset):
        json_project_ids = []
        for project_ids_item_data in project_ids:
            project_ids_item = str(project_ids_item_data)
            json_project_ids.append(project_ids_item)

    params["project_ids"] = json_project_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sources/import",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["SourceSchema"]]]:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = SourceSchema.from_dict(response_201_item_data)

            response_201.append(response_201_item)

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
) -> Response[Union[HTTPValidationError, list["SourceSchema"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyImportSourceSourcesImportPost,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
    project_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[HTTPValidationError, list["SourceSchema"]]]:
    """Import Source

     Import sources from a JSON file.

    This endpoint processes a JSON file containing source data and creates new sources in the system.
    The file must follow the expected format and contain valid source configurations. Only JSON files
    are accepted, and the data must match the system's source schema requirements.

    Args:
    - **file**: A JSON file containing source data to be imported.

    Returns:
    - **list[SourceSchema]**: List of sources that were successfully imported.

    Raises:
    - **400 Bad Request (InvalidParamsForImportException)**: Raised if the source_type or params in the
    given file are invalid.
    - **413 File Too Big (FileTooBigException)**: Raised if the JSON file is too big!
    - **500 (FailedToExtractData)**: Raised if the JSON file is corrupted or cannot be parsed.

    Args:
        collection_ids (Union[Unset, list[UUID]]): List of collection Ids to attach source to
        project_ids (Union[Unset, list[UUID]]): List of project Ids to attach source to
        body (BodyImportSourceSourcesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SourceSchema']]]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_ids=collection_ids,
        project_ids=project_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: BodyImportSourceSourcesImportPost,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
    project_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[HTTPValidationError, list["SourceSchema"]]]:
    """Import Source

     Import sources from a JSON file.

    This endpoint processes a JSON file containing source data and creates new sources in the system.
    The file must follow the expected format and contain valid source configurations. Only JSON files
    are accepted, and the data must match the system's source schema requirements.

    Args:
    - **file**: A JSON file containing source data to be imported.

    Returns:
    - **list[SourceSchema]**: List of sources that were successfully imported.

    Raises:
    - **400 Bad Request (InvalidParamsForImportException)**: Raised if the source_type or params in the
    given file are invalid.
    - **413 File Too Big (FileTooBigException)**: Raised if the JSON file is too big!
    - **500 (FailedToExtractData)**: Raised if the JSON file is corrupted or cannot be parsed.

    Args:
        collection_ids (Union[Unset, list[UUID]]): List of collection Ids to attach source to
        project_ids (Union[Unset, list[UUID]]): List of project Ids to attach source to
        body (BodyImportSourceSourcesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SourceSchema']]
    """

    return sync_detailed(
        client=client,
        body=body,
        collection_ids=collection_ids,
        project_ids=project_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyImportSourceSourcesImportPost,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
    project_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[HTTPValidationError, list["SourceSchema"]]]:
    """Import Source

     Import sources from a JSON file.

    This endpoint processes a JSON file containing source data and creates new sources in the system.
    The file must follow the expected format and contain valid source configurations. Only JSON files
    are accepted, and the data must match the system's source schema requirements.

    Args:
    - **file**: A JSON file containing source data to be imported.

    Returns:
    - **list[SourceSchema]**: List of sources that were successfully imported.

    Raises:
    - **400 Bad Request (InvalidParamsForImportException)**: Raised if the source_type or params in the
    given file are invalid.
    - **413 File Too Big (FileTooBigException)**: Raised if the JSON file is too big!
    - **500 (FailedToExtractData)**: Raised if the JSON file is corrupted or cannot be parsed.

    Args:
        collection_ids (Union[Unset, list[UUID]]): List of collection Ids to attach source to
        project_ids (Union[Unset, list[UUID]]): List of project Ids to attach source to
        body (BodyImportSourceSourcesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SourceSchema']]]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_ids=collection_ids,
        project_ids=project_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BodyImportSourceSourcesImportPost,
    collection_ids: Union[Unset, list[UUID]] = UNSET,
    project_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[HTTPValidationError, list["SourceSchema"]]]:
    """Import Source

     Import sources from a JSON file.

    This endpoint processes a JSON file containing source data and creates new sources in the system.
    The file must follow the expected format and contain valid source configurations. Only JSON files
    are accepted, and the data must match the system's source schema requirements.

    Args:
    - **file**: A JSON file containing source data to be imported.

    Returns:
    - **list[SourceSchema]**: List of sources that were successfully imported.

    Raises:
    - **400 Bad Request (InvalidParamsForImportException)**: Raised if the source_type or params in the
    given file are invalid.
    - **413 File Too Big (FileTooBigException)**: Raised if the JSON file is too big!
    - **500 (FailedToExtractData)**: Raised if the JSON file is corrupted or cannot be parsed.

    Args:
        collection_ids (Union[Unset, list[UUID]]): List of collection Ids to attach source to
        project_ids (Union[Unset, list[UUID]]): List of project Ids to attach source to
        body (BodyImportSourceSourcesImportPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SourceSchema']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            collection_ids=collection_ids,
            project_ids=project_ids,
        )
    ).parsed
