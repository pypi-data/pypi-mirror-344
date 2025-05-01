from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_subreddit_info_schema import PaginatedResponseSubredditInfoSchema
from ...models.sort_order import SortOrder
from ...models.subreddits_sort_by import SubredditsSortBy
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    order_by: Union[Unset, SubredditsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    subreddit_name: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params["order_by"] = json_order_by

    json_order_direction: Union[Unset, str] = UNSET
    if not isinstance(order_direction, Unset):
        json_order_direction = order_direction.value

    params["order_direction"] = json_order_direction

    params["page"] = page

    params["per_page"] = per_page

    json_subreddit_name: Union[None, Unset, str]
    if isinstance(subreddit_name, Unset):
        json_subreddit_name = UNSET
    else:
        json_subreddit_name = subreddit_name
    params["subreddit_name"] = json_subreddit_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/subreddits",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]:
    if response.status_code == 200:
        response_200 = PaginatedResponseSubredditInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, SubredditsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    subreddit_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]:
    """Get Subreddits

     Get a list of subreddits with optional filters and pagination.

    This endpoint returns a paginated list of subreddits with optional filter subreddit name match.
    It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'members'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **subreddit_name**: Optional partial match filter for subreddit names.

    Returns:
    - **PaginatedResponse[SubredditInfoSchema]**: A paginated response containing subreddits
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        order_by (Union[Unset, SubredditsSortBy]): Enumeration class representing subreddits sort
            by options.

            Attributes:
                MEMBERS: Represents members sort by option.
                ONLINE_MEMBERS: Represents online members sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        subreddit_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]
    """

    kwargs = _get_kwargs(
        order_by=order_by,
        order_direction=order_direction,
        page=page,
        per_page=per_page,
        subreddit_name=subreddit_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, SubredditsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    subreddit_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]:
    """Get Subreddits

     Get a list of subreddits with optional filters and pagination.

    This endpoint returns a paginated list of subreddits with optional filter subreddit name match.
    It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'members'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **subreddit_name**: Optional partial match filter for subreddit names.

    Returns:
    - **PaginatedResponse[SubredditInfoSchema]**: A paginated response containing subreddits
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        order_by (Union[Unset, SubredditsSortBy]): Enumeration class representing subreddits sort
            by options.

            Attributes:
                MEMBERS: Represents members sort by option.
                ONLINE_MEMBERS: Represents online members sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        subreddit_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]
    """

    return sync_detailed(
        client=client,
        order_by=order_by,
        order_direction=order_direction,
        page=page,
        per_page=per_page,
        subreddit_name=subreddit_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, SubredditsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    subreddit_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]:
    """Get Subreddits

     Get a list of subreddits with optional filters and pagination.

    This endpoint returns a paginated list of subreddits with optional filter subreddit name match.
    It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'members'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **subreddit_name**: Optional partial match filter for subreddit names.

    Returns:
    - **PaginatedResponse[SubredditInfoSchema]**: A paginated response containing subreddits
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        order_by (Union[Unset, SubredditsSortBy]): Enumeration class representing subreddits sort
            by options.

            Attributes:
                MEMBERS: Represents members sort by option.
                ONLINE_MEMBERS: Represents online members sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        subreddit_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]
    """

    kwargs = _get_kwargs(
        order_by=order_by,
        order_direction=order_direction,
        page=page,
        per_page=per_page,
        subreddit_name=subreddit_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    order_by: Union[Unset, SubredditsSortBy] = UNSET,
    order_direction: Union[Unset, SortOrder] = UNSET,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
    subreddit_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]]:
    """Get Subreddits

     Get a list of subreddits with optional filters and pagination.

    This endpoint returns a paginated list of subreddits with optional filter subreddit name match.
    It supports sorting by different fields and directions.

    Args:
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.
    - **order_by**: Field to sort the results by, default is 'members'.
    - **order_direction**: Sorting direction, either ascending or descending, default is 'DESC'.
    - **subreddit_name**: Optional partial match filter for subreddit names.

    Returns:
    - **PaginatedResponse[SubredditInfoSchema]**: A paginated response containing subreddits
    information.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents matching the search criteria are
    found.

    Args:
        order_by (Union[Unset, SubredditsSortBy]): Enumeration class representing subreddits sort
            by options.

            Attributes:
                MEMBERS: Represents members sort by option.
                ONLINE_MEMBERS: Represents online members sort by option.
                NONE: Represents none sort by option.
        order_direction (Union[Unset, SortOrder]): Enumeration class representing sort order
            options.

            Attributes:
                ASC: Represents ascending sort order option.
                DESC: Represents descending sort order option.
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.
        subreddit_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseSubredditInfoSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
            subreddit_name=subreddit_name,
        )
    ).parsed
