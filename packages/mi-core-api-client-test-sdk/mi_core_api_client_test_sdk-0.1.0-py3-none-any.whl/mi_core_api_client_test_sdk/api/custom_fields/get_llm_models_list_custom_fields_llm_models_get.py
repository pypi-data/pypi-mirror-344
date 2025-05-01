from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_with_metadata_schemalist_open_router_model_info import (
    ResponseWithMetadataSchemalistOpenRouterModelInfo,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/custom-fields/llm/models",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ResponseWithMetadataSchemalistOpenRouterModelInfo]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistOpenRouterModelInfo.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResponseWithMetadataSchemalistOpenRouterModelInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemalistOpenRouterModelInfo]:
    """Get Llm Models List

     Get a list of available LLM models from OpenRouter.

    Returns:
    - **list[OpenRouterModelInfo]**: A list of schemas containing information about the available LLM
    models and their detailed description.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **400 Bad Request (MissingResponseException)**: Raised if OpenRouter response does not contain
    expected 'data' field.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemalistOpenRouterModelInfo]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemalistOpenRouterModelInfo]:
    """Get Llm Models List

     Get a list of available LLM models from OpenRouter.

    Returns:
    - **list[OpenRouterModelInfo]**: A list of schemas containing information about the available LLM
    models and their detailed description.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **400 Bad Request (MissingResponseException)**: Raised if OpenRouter response does not contain
    expected 'data' field.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemalistOpenRouterModelInfo
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResponseWithMetadataSchemalistOpenRouterModelInfo]:
    """Get Llm Models List

     Get a list of available LLM models from OpenRouter.

    Returns:
    - **list[OpenRouterModelInfo]**: A list of schemas containing information about the available LLM
    models and their detailed description.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **400 Bad Request (MissingResponseException)**: Raised if OpenRouter response does not contain
    expected 'data' field.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseWithMetadataSchemalistOpenRouterModelInfo]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[ResponseWithMetadataSchemalistOpenRouterModelInfo]:
    """Get Llm Models List

     Get a list of available LLM models from OpenRouter.

    Returns:
    - **list[OpenRouterModelInfo]**: A list of schemas containing information about the available LLM
    models and their detailed description.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **400 Bad Request (MissingResponseException)**: Raised if OpenRouter response does not contain
    expected 'data' field.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseWithMetadataSchemalistOpenRouterModelInfo
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
