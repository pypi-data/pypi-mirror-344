from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_g_trend_interest_over_time_dto import (
    ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO,
)
from ...models.time_range import TimeRange
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    queries: Union[Unset, str] = "coffee,milk,bread,pasta,steak",
    time_range: Union[Unset, TimeRange] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["queries"] = queries

    json_time_range: Union[Unset, str] = UNSET
    if not isinstance(time_range, Unset):
        json_time_range = time_range.value

    params["time_range"] = json_time_range

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/gtrends/overtime",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    queries: Union[Unset, str] = "coffee,milk,bread,pasta,steak",
    time_range: Union[Unset, TimeRange] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]:
    """Get Gtrend Overtime

    Args:
        queries (Union[Unset, str]):  Default: 'coffee,milk,bread,pasta,steak'.
        time_range (Union[Unset, TimeRange]): Enumeration class representing time range options.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        time_range=time_range,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    queries: Union[Unset, str] = "coffee,milk,bread,pasta,steak",
    time_range: Union[Unset, TimeRange] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]:
    """Get Gtrend Overtime

    Args:
        queries (Union[Unset, str]):  Default: 'coffee,milk,bread,pasta,steak'.
        time_range (Union[Unset, TimeRange]): Enumeration class representing time range options.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]
    """

    return sync_detailed(
        client=client,
        queries=queries,
        time_range=time_range,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    queries: Union[Unset, str] = "coffee,milk,bread,pasta,steak",
    time_range: Union[Unset, TimeRange] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]:
    """Get Gtrend Overtime

    Args:
        queries (Union[Unset, str]):  Default: 'coffee,milk,bread,pasta,steak'.
        time_range (Union[Unset, TimeRange]): Enumeration class representing time range options.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        time_range=time_range,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    queries: Union[Unset, str] = "coffee,milk,bread,pasta,steak",
    time_range: Union[Unset, TimeRange] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]]:
    """Get Gtrend Overtime

    Args:
        queries (Union[Unset, str]):  Default: 'coffee,milk,bread,pasta,steak'.
        time_range (Union[Unset, TimeRange]): Enumeration class representing time range options.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendInterestOverTimeDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            queries=queries,
            time_range=time_range,
        )
    ).parsed
