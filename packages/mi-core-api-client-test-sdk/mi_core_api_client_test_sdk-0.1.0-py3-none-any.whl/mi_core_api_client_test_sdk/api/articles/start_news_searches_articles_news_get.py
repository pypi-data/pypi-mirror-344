import datetime
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
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, str] = "google",
    tbm: Union[Unset, str] = "nws",
    q: list[str],
    timeframe: Union[Unset, list[datetime.date]] = UNSET,
    num_results: Union[Unset, int] = 10,
    offset: Union[Unset, int] = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["use_cache"] = use_cache

    params["engine"] = engine

    params["tbm"] = tbm

    json_q = q

    params["q"] = json_q

    json_timeframe: Union[Unset, list[str]] = UNSET
    if not isinstance(timeframe, Unset):
        json_timeframe = []
        for timeframe_item_data in timeframe:
            timeframe_item = timeframe_item_data.isoformat()
            json_timeframe.append(timeframe_item)

    params["timeframe"] = json_timeframe

    params["num_results"] = num_results

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/articles/news",
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
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, str] = "google",
    tbm: Union[Unset, str] = "nws",
    q: list[str],
    timeframe: Union[Unset, list[datetime.date]] = UNSET,
    num_results: Union[Unset, int] = 10,
    offset: Union[Unset, int] = 0,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    r"""Start News Searches

     Starts news articles search based on the provided queries and search parameters.

    Args:
    - **use_cache**: Flag indicating whether to use cached results, default is True.
    - **engine**: The search engine to use for the query, default is \"google\".
    - **tbm**: The type of search (e.g., 'nws' for news), default is \"nws\".
    - **q**: List of search queries.
    - **timeframe**: A list of dates to filter the search results.
    - **num_results**: The number of search results to retrieve, default is 10, minimum is 10, maximum
    is 100.
    - **offset**: Offset for paginated search results, default is 0.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of aggregated news articles or error details.

    Raises:
    - **400 Bad Request (ValueError)**: Raised if any of the query parameters are invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no search results are found.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, str]): Search engine to use Default: 'google'.
        tbm (Union[Unset, str]): Type of search (e.g., 'nws' for news) Default: 'nws'.
        q (list[str]):
        timeframe (Union[Unset, list[datetime.date]]):
        num_results (Union[Unset, int]):  Default: 10.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        use_cache=use_cache,
        engine=engine,
        tbm=tbm,
        q=q,
        timeframe=timeframe,
        num_results=num_results,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, str] = "google",
    tbm: Union[Unset, str] = "nws",
    q: list[str],
    timeframe: Union[Unset, list[datetime.date]] = UNSET,
    num_results: Union[Unset, int] = 10,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    r"""Start News Searches

     Starts news articles search based on the provided queries and search parameters.

    Args:
    - **use_cache**: Flag indicating whether to use cached results, default is True.
    - **engine**: The search engine to use for the query, default is \"google\".
    - **tbm**: The type of search (e.g., 'nws' for news), default is \"nws\".
    - **q**: List of search queries.
    - **timeframe**: A list of dates to filter the search results.
    - **num_results**: The number of search results to retrieve, default is 10, minimum is 10, maximum
    is 100.
    - **offset**: Offset for paginated search results, default is 0.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of aggregated news articles or error details.

    Raises:
    - **400 Bad Request (ValueError)**: Raised if any of the query parameters are invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no search results are found.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, str]): Search engine to use Default: 'google'.
        tbm (Union[Unset, str]): Type of search (e.g., 'nws' for news) Default: 'nws'.
        q (list[str]):
        timeframe (Union[Unset, list[datetime.date]]):
        num_results (Union[Unset, int]):  Default: 10.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]
    """

    return sync_detailed(
        client=client,
        use_cache=use_cache,
        engine=engine,
        tbm=tbm,
        q=q,
        timeframe=timeframe,
        num_results=num_results,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, str] = "google",
    tbm: Union[Unset, str] = "nws",
    q: list[str],
    timeframe: Union[Unset, list[datetime.date]] = UNSET,
    num_results: Union[Unset, int] = 10,
    offset: Union[Unset, int] = 0,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    r"""Start News Searches

     Starts news articles search based on the provided queries and search parameters.

    Args:
    - **use_cache**: Flag indicating whether to use cached results, default is True.
    - **engine**: The search engine to use for the query, default is \"google\".
    - **tbm**: The type of search (e.g., 'nws' for news), default is \"nws\".
    - **q**: List of search queries.
    - **timeframe**: A list of dates to filter the search results.
    - **num_results**: The number of search results to retrieve, default is 10, minimum is 10, maximum
    is 100.
    - **offset**: Offset for paginated search results, default is 0.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of aggregated news articles or error details.

    Raises:
    - **400 Bad Request (ValueError)**: Raised if any of the query parameters are invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no search results are found.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, str]): Search engine to use Default: 'google'.
        tbm (Union[Unset, str]): Type of search (e.g., 'nws' for news) Default: 'nws'.
        q (list[str]):
        timeframe (Union[Unset, list[datetime.date]]):
        num_results (Union[Unset, int]):  Default: 10.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]
    """

    kwargs = _get_kwargs(
        use_cache=use_cache,
        engine=engine,
        tbm=tbm,
        q=q,
        timeframe=timeframe,
        num_results=num_results,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    use_cache: Union[Unset, bool] = True,
    engine: Union[Unset, str] = "google",
    tbm: Union[Unset, str] = "nws",
    q: list[str],
    timeframe: Union[Unset, list[datetime.date]] = UNSET,
    num_results: Union[Unset, int] = 10,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]]:
    r"""Start News Searches

     Starts news articles search based on the provided queries and search parameters.

    Args:
    - **use_cache**: Flag indicating whether to use cached results, default is True.
    - **engine**: The search engine to use for the query, default is \"google\".
    - **tbm**: The type of search (e.g., 'nws' for news), default is \"nws\".
    - **q**: List of search queries.
    - **timeframe**: A list of dates to filter the search results.
    - **num_results**: The number of search results to retrieve, default is 10, minimum is 10, maximum
    is 100.
    - **offset**: Offset for paginated search results, default is 0.

    Returns:
    - **list[Union[ArticleSchema, ErrorDTO]]**: A list of aggregated news articles or error details.

    Raises:
    - **400 Bad Request (ValueError)**: Raised if any of the query parameters are invalid.
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **404 Not Found (ObjectNotFound)**: Raised if no result is found based on the statement.
    - **404 Not Found (ArticleResultNotFoundException)**: Raised if no search results are found.
    - **500 Internal Server Error (FailedToExtractData)**: Raised if there is a failure during data
    extraction.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    error during retrieval.

    Args:
        use_cache (Union[Unset, bool]):  Default: True.
        engine (Union[Unset, str]): Search engine to use Default: 'google'.
        tbm (Union[Unset, str]): Type of search (e.g., 'nws' for news) Default: 'nws'.
        q (list[str]):
        timeframe (Union[Unset, list[datetime.date]]):
        num_results (Union[Unset, int]):  Default: 10.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistUnionArticleSchemaErrorDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            use_cache=use_cache,
            engine=engine,
            tbm=tbm,
            q=q,
            timeframe=timeframe,
            num_results=num_results,
            offset=offset,
        )
    ).parsed
