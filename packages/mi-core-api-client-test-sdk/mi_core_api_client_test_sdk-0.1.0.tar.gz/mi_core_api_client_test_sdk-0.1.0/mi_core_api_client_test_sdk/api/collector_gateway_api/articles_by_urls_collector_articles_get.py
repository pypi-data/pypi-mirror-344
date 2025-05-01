from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_article_gateway_error_dto import (
    ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO,
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
        "url": "/collector/articles",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]:
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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]:
    """Articles By Urls

     Retrieve articles by their URLs.

    This endpoint fetches the content of articles from the specified URLs using the gateway service.

    Args:
    - **urls**: A list of URLs to fetch the article content from.

    Returns:
    - **list[Article | GatewayErrorDTO]**: A list of articles or error objects if any issues occur.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the input URLs are not valid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]
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
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]:
    """Articles By Urls

     Retrieve articles by their URLs.

    This endpoint fetches the content of articles from the specified URLs using the gateway service.

    Args:
    - **urls**: A list of URLs to fetch the article content from.

    Returns:
    - **list[Article | GatewayErrorDTO]**: A list of articles or error objects if any issues occur.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the input URLs are not valid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]
    """

    return sync_detailed(
        client=client,
        urls=urls,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    urls: list[str],
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]:
    """Articles By Urls

     Retrieve articles by their URLs.

    This endpoint fetches the content of articles from the specified URLs using the gateway service.

    Args:
    - **urls**: A list of URLs to fetch the article content from.

    Returns:
    - **list[Article | GatewayErrorDTO]**: A list of articles or error objects if any issues occur.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the input URLs are not valid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]
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
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]]:
    """Articles By Urls

     Retrieve articles by their URLs.

    This endpoint fetches the content of articles from the specified URLs using the gateway service.

    Args:
    - **urls**: A list of URLs to fetch the article content from.

    Returns:
    - **list[Article | GatewayErrorDTO]**: A list of articles or error objects if any issues occur.

    Raises:
    - **400 Bad Request (InvalidURLException)**: Raised if the input URLs are not valid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key or token does not have the
    required permissions, is expired or invalid.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ResultNotFoundException)**: Raised if the requested resource is not found in the
    gateway.
    - **500 Internal Server Error (MissingResponseException)**: Raised if the gateway does not return a
    valid response.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        urls (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleGatewayErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            urls=urls,
        )
    ).parsed
