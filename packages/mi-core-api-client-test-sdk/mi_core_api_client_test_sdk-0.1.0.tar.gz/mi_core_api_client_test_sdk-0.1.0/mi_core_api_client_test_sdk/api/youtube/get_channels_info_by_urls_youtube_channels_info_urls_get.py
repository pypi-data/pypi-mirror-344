from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_youtube_channel_info_schema_error_dto import (
    ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO,
)
from ...types import UNSET, Response


def _get_kwargs(
    *,
    urls: list[str],
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_urls = urls

    params["urls"] = json_urls

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/youtube/channels/info/urls",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    urls: list[str],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]:
    """Get Channels Info By Urls

     Retrieves information about YouTube channels based on their URLs.

    This endpoint fetches YouTube channel information for the specified list of channel URLs.
    It also supports caching to avoid redundant requests.

    Args:
    - **urls**: A list of YouTube channel URLs to retrieve information for.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[YoutubeChannelInfoSchema, ErrorDTO]]**:
        A schema containing channel details or error information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        urls=urls,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    urls: list[str],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]:
    """Get Channels Info By Urls

     Retrieves information about YouTube channels based on their URLs.

    This endpoint fetches YouTube channel information for the specified list of channel URLs.
    It also supports caching to avoid redundant requests.

    Args:
    - **urls**: A list of YouTube channel URLs to retrieve information for.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[YoutubeChannelInfoSchema, ErrorDTO]]**:
        A schema containing channel details or error information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]
    """

    return sync_detailed(
        client=client,
        urls=urls,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    urls: list[str],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]:
    """Get Channels Info By Urls

     Retrieves information about YouTube channels based on their URLs.

    This endpoint fetches YouTube channel information for the specified list of channel URLs.
    It also supports caching to avoid redundant requests.

    Args:
    - **urls**: A list of YouTube channel URLs to retrieve information for.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[YoutubeChannelInfoSchema, ErrorDTO]]**:
        A schema containing channel details or error information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        urls=urls,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    urls: list[str],
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]]:
    """Get Channels Info By Urls

     Retrieves information about YouTube channels based on their URLs.

    This endpoint fetches YouTube channel information for the specified list of channel URLs.
    It also supports caching to avoid redundant requests.

    Args:
    - **urls**: A list of YouTube channel URLs to retrieve information for.
    - **use_cache**: Boolean indicating whether to use cached data, default is True.

    Returns:
    - **list[Union[YoutubeChannelInfoSchema, ErrorDTO]]**:
        A schema containing channel details or error information.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ChannelNotFoundException)**: Raised if no URL is found for the specified channel
    name.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if an error occurs while processing or
    extracting data.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (APIMethodException)**: Raised if an error occurs while using the API
    method to collect data.
    - **500 Internal Server Error (HTMLMethodException)**: Raised if an error occurs while using the
    HTML method to collect data.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionYoutubeChannelInfoSchemaErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            urls=urls,
        )
    ).parsed
