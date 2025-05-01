from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.custom_field_type import CustomFieldType
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemadictstr_liststr import ResponseWithMetadataSchemadictstrListstr
from ...types import UNSET, Response


def _get_kwargs(
    *,
    content_type: CustomFieldType,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_content_type = content_type.value
    params["content_type"] = json_content_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/custom-fields/prompt-fields",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemadictstrListstr.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    content_type: CustomFieldType,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]:
    """Get Prompt Fields

     Get a list of available variables for prompt.

    Args:
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **dict[str, list[str]]**: The available variables information for the prompt, where key is
    document type and value its relevant fields.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]
    """

    kwargs = _get_kwargs(
        content_type=content_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    content_type: CustomFieldType,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]:
    """Get Prompt Fields

     Get a list of available variables for prompt.

    Args:
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **dict[str, list[str]]**: The available variables information for the prompt, where key is
    document type and value its relevant fields.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]
    """

    return sync_detailed(
        client=client,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    content_type: CustomFieldType,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]:
    """Get Prompt Fields

     Get a list of available variables for prompt.

    Args:
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **dict[str, list[str]]**: The available variables information for the prompt, where key is
    document type and value its relevant fields.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]
    """

    kwargs = _get_kwargs(
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    content_type: CustomFieldType,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]]:
    """Get Prompt Fields

     Get a list of available variables for prompt.

    Args:
    - **content_type**: The type of content to extract values from (e.g. content or comment).

    Returns:
    - **dict[str, list[str]]**: The available variables information for the prompt, where key is
    document type and value its relevant fields.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.

    Args:
        content_type (CustomFieldType): Enumeration class representing custom field types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListstr]
    """

    return (
        await asyncio_detailed(
            client=client,
            content_type=content_type,
        )
    ).parsed
