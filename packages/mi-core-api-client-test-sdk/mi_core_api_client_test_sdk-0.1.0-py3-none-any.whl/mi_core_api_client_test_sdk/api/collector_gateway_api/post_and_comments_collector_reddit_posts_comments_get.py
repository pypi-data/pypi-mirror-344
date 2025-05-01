from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.extract_method import ExtractMethod
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_union_gateway_reddit_posts_and_comments_dto_gateway_error_dto import (
    ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    urls: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    with_comments: Union[Unset, bool] = True,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_extract_method: Union[Unset, str] = UNSET
    if not isinstance(extract_method, Unset):
        json_extract_method = extract_method.value

    params["extract_method"] = json_extract_method

    json_urls = urls

    params["urls"] = json_urls

    params["max_duration_sec"] = max_duration_sec

    params["with_comments"] = with_comments

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/collector/reddit/posts/comments",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO.from_dict(
            response.json()
        )

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
) -> Response[
    Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    urls: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    with_comments: Union[Unset, bool] = True,
) -> Response[
    Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
]:
    """Post And Comments

     Retrieve Reddit posts and comments.

    Fetches both the Reddit posts and their comments from the provided URLs.

    Args:
    - **extract_method**: The method used to extract data (e.g., API).
    - **urls**: A list of URLs to fetch posts and comments from.
    - **max_duration_sec**: Maximum time in seconds for the extraction process.
    - **with_comments**: Whether to retrieve the comments along with the posts.

    Returns:
    - **list[GatewayRedditPostsAndCommentsDTO | GatewayErrorDTO]**: A list of posts with comments or
    error objects.

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
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        urls (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        with_comments (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]]
    """

    kwargs = _get_kwargs(
        extract_method=extract_method,
        urls=urls,
        max_duration_sec=max_duration_sec,
        with_comments=with_comments,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    urls: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    with_comments: Union[Unset, bool] = True,
) -> Optional[
    Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
]:
    """Post And Comments

     Retrieve Reddit posts and comments.

    Fetches both the Reddit posts and their comments from the provided URLs.

    Args:
    - **extract_method**: The method used to extract data (e.g., API).
    - **urls**: A list of URLs to fetch posts and comments from.
    - **max_duration_sec**: Maximum time in seconds for the extraction process.
    - **with_comments**: Whether to retrieve the comments along with the posts.

    Returns:
    - **list[GatewayRedditPostsAndCommentsDTO | GatewayErrorDTO]**: A list of posts with comments or
    error objects.

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
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        urls (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        with_comments (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
    """

    return sync_detailed(
        client=client,
        extract_method=extract_method,
        urls=urls,
        max_duration_sec=max_duration_sec,
        with_comments=with_comments,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    urls: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    with_comments: Union[Unset, bool] = True,
) -> Response[
    Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
]:
    """Post And Comments

     Retrieve Reddit posts and comments.

    Fetches both the Reddit posts and their comments from the provided URLs.

    Args:
    - **extract_method**: The method used to extract data (e.g., API).
    - **urls**: A list of URLs to fetch posts and comments from.
    - **max_duration_sec**: Maximum time in seconds for the extraction process.
    - **with_comments**: Whether to retrieve the comments along with the posts.

    Returns:
    - **list[GatewayRedditPostsAndCommentsDTO | GatewayErrorDTO]**: A list of posts with comments or
    error objects.

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
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        urls (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        with_comments (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]]
    """

    kwargs = _get_kwargs(
        extract_method=extract_method,
        urls=urls,
        max_duration_sec=max_duration_sec,
        with_comments=with_comments,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    extract_method: Union[Unset, ExtractMethod] = UNSET,
    urls: list[str],
    max_duration_sec: Union[Unset, int] = 60,
    with_comments: Union[Unset, bool] = True,
) -> Optional[
    Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
]:
    """Post And Comments

     Retrieve Reddit posts and comments.

    Fetches both the Reddit posts and their comments from the provided URLs.

    Args:
    - **extract_method**: The method used to extract data (e.g., API).
    - **urls**: A list of URLs to fetch posts and comments from.
    - **max_duration_sec**: Maximum time in seconds for the extraction process.
    - **with_comments**: Whether to retrieve the comments along with the posts.

    Returns:
    - **list[GatewayRedditPostsAndCommentsDTO | GatewayErrorDTO]**: A list of posts with comments or
    error objects.

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
        extract_method (Union[Unset, ExtractMethod]): Enumeration defining methods for extracting
            data.

            Attributes:
                HTML: Represents HTML extraction method.
                API: Represents API extraction method.
        urls (list[str]):
        max_duration_sec (Union[Unset, int]):  Default: 60.
        with_comments (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionGatewayRedditPostsAndCommentsDTOGatewayErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            extract_method=extract_method,
            urls=urls,
            max_duration_sec=max_duration_sec,
            with_comments=with_comments,
        )
    ).parsed
