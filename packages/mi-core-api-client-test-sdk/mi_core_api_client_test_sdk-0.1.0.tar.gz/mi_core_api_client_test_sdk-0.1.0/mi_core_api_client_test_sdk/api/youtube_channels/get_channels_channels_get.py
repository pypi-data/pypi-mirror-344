from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.channels_sort_by import ChannelsSortBy
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_youtube_channel_info_schema import PaginatedResponseYoutubeChannelInfoSchema
from ...models.sort_order import SortOrder
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    order_by: Union[Unset, ChannelsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    channel_name: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["per_page"] = per_page

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params["order_by"] = json_order_by

    json_order_direction: Union[Unset, str] = UNSET
    if not isinstance(order_direction, Unset):
        json_order_direction = order_direction.value

    params["order_direction"] = json_order_direction

    json_country: Union[None, Unset, str]
    if isinstance(country, Unset):
        json_country = UNSET
    else:
        json_country = country
    params["country"] = json_country

    json_channel_name: Union[None, Unset, str]
    if isinstance(channel_name, Unset):
        json_channel_name = UNSET
    else:
        json_channel_name = channel_name
    params["channel_name"] = json_channel_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/channels",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseYoutubeChannelInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    order_by: Union[Unset, ChannelsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    channel_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]:
    """Get Channels

     Get a list of YouTube channels with optional filters and pagination.

    This endpoint returns a paginated list of YouTube channels with optional filters such as
    country and partial channel name match. It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'subscribers'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **country**: Optional country filter.
    - **channel_name**: Optional partial match filter for channel names.

    Returns:
    - **PaginatedResponse[YoutubeChannelInfoSchema]**: A paginated response containing YouTube channel
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        order_by (Union[Unset, ChannelsSortBy]): Enumeration class representing channels sort by
            options.

            Attributes:
                TOTAL_VIDEOS: Represents total videos sort by option.
                SUBSCRIBERS: Represents subscribers sort by option.
                TOTAL_VIEWS: Represents total views sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        country (Union[None, Unset, str]):
        channel_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        order_by=order_by,
        order_direction=order_direction,
        country=country,
        channel_name=channel_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    order_by: Union[Unset, ChannelsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    channel_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]:
    """Get Channels

     Get a list of YouTube channels with optional filters and pagination.

    This endpoint returns a paginated list of YouTube channels with optional filters such as
    country and partial channel name match. It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'subscribers'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **country**: Optional country filter.
    - **channel_name**: Optional partial match filter for channel names.

    Returns:
    - **PaginatedResponse[YoutubeChannelInfoSchema]**: A paginated response containing YouTube channel
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        order_by (Union[Unset, ChannelsSortBy]): Enumeration class representing channels sort by
            options.

            Attributes:
                TOTAL_VIDEOS: Represents total videos sort by option.
                SUBSCRIBERS: Represents subscribers sort by option.
                TOTAL_VIEWS: Represents total views sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        country (Union[None, Unset, str]):
        channel_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]
    """

    return sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        order_by=order_by,
        order_direction=order_direction,
        country=country,
        channel_name=channel_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    order_by: Union[Unset, ChannelsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    channel_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]:
    """Get Channels

     Get a list of YouTube channels with optional filters and pagination.

    This endpoint returns a paginated list of YouTube channels with optional filters such as
    country and partial channel name match. It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'subscribers'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **country**: Optional country filter.
    - **channel_name**: Optional partial match filter for channel names.

    Returns:
    - **PaginatedResponse[YoutubeChannelInfoSchema]**: A paginated response containing YouTube channel
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        order_by (Union[Unset, ChannelsSortBy]): Enumeration class representing channels sort by
            options.

            Attributes:
                TOTAL_VIDEOS: Represents total videos sort by option.
                SUBSCRIBERS: Represents subscribers sort by option.
                TOTAL_VIEWS: Represents total views sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        country (Union[None, Unset, str]):
        channel_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]
    """

    kwargs = _get_kwargs(
        page=page,
        per_page=per_page,
        order_by=order_by,
        order_direction=order_direction,
        country=country,
        channel_name=channel_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    order_by: Union[Unset, ChannelsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    country: Union[None, Unset, str] = UNSET,
    channel_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]]:
    """Get Channels

     Get a list of YouTube channels with optional filters and pagination.

    This endpoint returns a paginated list of YouTube channels with optional filters such as
    country and partial channel name match. It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'subscribers'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **country**: Optional country filter.
    - **channel_name**: Optional partial match filter for channel names.

    Returns:
    - **PaginatedResponse[YoutubeChannelInfoSchema]**: A paginated response containing YouTube channel
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        order_by (Union[Unset, ChannelsSortBy]): Enumeration class representing channels sort by
            options.

            Attributes:
                TOTAL_VIDEOS: Represents total videos sort by option.
                SUBSCRIBERS: Represents subscribers sort by option.
                TOTAL_VIEWS: Represents total views sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        country (Union[None, Unset, str]):
        channel_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseYoutubeChannelInfoSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
            country=country,
            channel_name=channel_name,
        )
    ).parsed
