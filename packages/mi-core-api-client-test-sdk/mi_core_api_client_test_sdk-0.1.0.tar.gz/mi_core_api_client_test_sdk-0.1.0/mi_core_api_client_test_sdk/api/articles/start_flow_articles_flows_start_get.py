from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_article_schema_error_dto import (
    ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    dates: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_dates: Union[Unset, list[str]] = UNSET
    if not isinstance(dates, Unset):
        json_dates = dates

    params["dates"] = json_dates

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/articles/flows/start",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[str]] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    """Start Flow

     Initiates the flow process for given dates and returns aggregated results.

    This endpoint triggers the flow process for a list of dates. The flow service handles
    the extraction and processing of articles based on the provided dates.

    Args:
    - **dates**: A list of dates to process. Defaults to today's date.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of processed articles or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no articles are found for the
    provided URLs.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        dates (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        dates=dates,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    """Start Flow

     Initiates the flow process for given dates and returns aggregated results.

    This endpoint triggers the flow process for a list of dates. The flow service handles
    the extraction and processing of articles based on the provided dates.

    Args:
    - **dates**: A list of dates to process. Defaults to today's date.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of processed articles or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no articles are found for the
    provided URLs.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        dates (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]
    """

    return sync_detailed(
        client=client,
        dates=dates,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[str]] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    """Start Flow

     Initiates the flow process for given dates and returns aggregated results.

    This endpoint triggers the flow process for a list of dates. The flow service handles
    the extraction and processing of articles based on the provided dates.

    Args:
    - **dates**: A list of dates to process. Defaults to today's date.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of processed articles or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no articles are found for the
    provided URLs.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        dates (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        dates=dates,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    """Start Flow

     Initiates the flow process for given dates and returns aggregated results.

    This endpoint triggers the flow process for a list of dates. The flow service handles
    the extraction and processing of articles based on the provided dates.

    Args:
    - **dates**: A list of dates to process. Defaults to today's date.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of processed articles or error details.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no articles are found for the
    provided URLs.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (ValueError)**: Raised if the filter operator is not supported or the
    column is invalid.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        dates (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            dates=dates,
        )
    ).parsed
