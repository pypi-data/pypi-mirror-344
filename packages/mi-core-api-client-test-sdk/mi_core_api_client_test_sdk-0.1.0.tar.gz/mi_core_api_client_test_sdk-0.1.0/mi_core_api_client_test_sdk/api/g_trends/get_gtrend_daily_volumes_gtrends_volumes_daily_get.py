import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_g_trend_daily_volume_in_db import (
    ResponseWithMetadataSchemalistGTrendDailyVolumeInDB,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    dates: Union[Unset, list[datetime.date]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_dates: Union[Unset, list[str]] = UNSET
    if not isinstance(dates, Unset):
        json_dates = []
        for dates_item_data in dates:
            dates_item = dates_item_data.isoformat()
            json_dates.append(dates_item)

    params["dates"] = json_dates

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/gtrends/volumes/daily",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistGTrendDailyVolumeInDB.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[datetime.date]] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]:
    """Get Gtrend Daily Volumes

     Get Google Trends daily volumes for a list of dates.

    This endpoint retrieves Google Trends daily volumes for each date passed in the query parameter
    dates.
    If no date is provided, it defaults to the current date.

    Args:
    - **dates**: A list of dates to retrieve daily trends volumes for. Defaults to today's date.

    Returns:
    - **list[GTrendDailyVolumeInDB]**: A list of Google Trends daily volumes for the given dates.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the API key or bearer token is invalid or
    expired.
    - **401 Unauthorized (CredentialException)**: Raised if the bearer token is invalid or the user is
    not found in Firebase.
    - **404 Not Found (ObjectNotFound)**: Raised if no Google Trends volumes are found for the provided
    dates.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    issue.

    Args:
        dates (Union[Unset, list[datetime.date]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]
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
    dates: Union[Unset, list[datetime.date]] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]:
    """Get Gtrend Daily Volumes

     Get Google Trends daily volumes for a list of dates.

    This endpoint retrieves Google Trends daily volumes for each date passed in the query parameter
    dates.
    If no date is provided, it defaults to the current date.

    Args:
    - **dates**: A list of dates to retrieve daily trends volumes for. Defaults to today's date.

    Returns:
    - **list[GTrendDailyVolumeInDB]**: A list of Google Trends daily volumes for the given dates.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the API key or bearer token is invalid or
    expired.
    - **401 Unauthorized (CredentialException)**: Raised if the bearer token is invalid or the user is
    not found in Firebase.
    - **404 Not Found (ObjectNotFound)**: Raised if no Google Trends volumes are found for the provided
    dates.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    issue.

    Args:
        dates (Union[Unset, list[datetime.date]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]
    """

    return sync_detailed(
        client=client,
        dates=dates,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[datetime.date]] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]:
    """Get Gtrend Daily Volumes

     Get Google Trends daily volumes for a list of dates.

    This endpoint retrieves Google Trends daily volumes for each date passed in the query parameter
    dates.
    If no date is provided, it defaults to the current date.

    Args:
    - **dates**: A list of dates to retrieve daily trends volumes for. Defaults to today's date.

    Returns:
    - **list[GTrendDailyVolumeInDB]**: A list of Google Trends daily volumes for the given dates.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the API key or bearer token is invalid or
    expired.
    - **401 Unauthorized (CredentialException)**: Raised if the bearer token is invalid or the user is
    not found in Firebase.
    - **404 Not Found (ObjectNotFound)**: Raised if no Google Trends volumes are found for the provided
    dates.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    issue.

    Args:
        dates (Union[Unset, list[datetime.date]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]
    """

    kwargs = _get_kwargs(
        dates=dates,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    dates: Union[Unset, list[datetime.date]] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]]:
    """Get Gtrend Daily Volumes

     Get Google Trends daily volumes for a list of dates.

    This endpoint retrieves Google Trends daily volumes for each date passed in the query parameter
    dates.
    If no date is provided, it defaults to the current date.

    Args:
    - **dates**: A list of dates to retrieve daily trends volumes for. Defaults to today's date.

    Returns:
    - **list[GTrendDailyVolumeInDB]**: A list of Google Trends daily volumes for the given dates.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the API key or bearer token is invalid or
    expired.
    - **401 Unauthorized (CredentialException)**: Raised if the bearer token is invalid or the user is
    not found in Firebase.
    - **404 Not Found (ObjectNotFound)**: Raised if no Google Trends volumes are found for the provided
    dates.
    - **500 Internal Server Error (DBConnectionException)**: Raised if there is a database connection
    issue.

    Args:
        dates (Union[Unset, list[datetime.date]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistGTrendDailyVolumeInDB]
    """

    return (
        await asyncio_detailed(
            client=client,
            dates=dates,
        )
    ).parsed
