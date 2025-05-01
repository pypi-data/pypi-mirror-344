from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_g_trend_interest_metrics_response import (
    ResponseWithMetadataSchemaGTrendInterestMetricsResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    query: Union[Unset, str] = "coffee",
    use_cache: Union[Unset, bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["query"] = query

    params["use_cache"] = use_cache

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/gtrends/interest",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaGTrendInterestMetricsResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "coffee",
    use_cache: Union[Unset, bool] = False,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]:
    """Get Gtrend Interest Metrics

    Args:
        query (Union[Unset, str]):  Default: 'coffee'.
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]
    """

    kwargs = _get_kwargs(
        query=query,
        use_cache=use_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "coffee",
    use_cache: Union[Unset, bool] = False,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]:
    """Get Gtrend Interest Metrics

    Args:
        query (Union[Unset, str]):  Default: 'coffee'.
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]
    """

    return sync_detailed(
        client=client,
        query=query,
        use_cache=use_cache,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "coffee",
    use_cache: Union[Unset, bool] = False,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]:
    """Get Gtrend Interest Metrics

    Args:
        query (Union[Unset, str]):  Default: 'coffee'.
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]
    """

    kwargs = _get_kwargs(
        query=query,
        use_cache=use_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    query: Union[Unset, str] = "coffee",
    use_cache: Union[Unset, bool] = False,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]]:
    """Get Gtrend Interest Metrics

    Args:
        query (Union[Unset, str]):  Default: 'coffee'.
        use_cache (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaGTrendInterestMetricsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            use_cache=use_cache,
        )
    ).parsed
