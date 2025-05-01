from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.searchbar_item_dto import SearchbarItemDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    limit: Union[Unset, int] = 5,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["q"] = q

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/documents/search/suggestions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["SearchbarItemDTO"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SearchbarItemDTO.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["SearchbarItemDTO"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    q: str,
    limit: Union[Unset, int] = 5,
) -> Response[Union[HTTPValidationError, list["SearchbarItemDTO"]]]:
    """Get Searchbar Suggestion

     Get search suggestions for a given query.

    This endpoint provides search suggestions based on the query string. The results are filtered and
    sorted.

    Args:
    - **q**: The search query to get suggestions for.
    - **limit**: The maximum number of suggestions to return, default is 5.

    Returns:
    - **list[SearchbarItemDTO]**: A list of search suggestion items.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if no data matching the search query is found.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        q (str):
        limit (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SearchbarItemDTO']]]
    """

    kwargs = _get_kwargs(
        q=q,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    q: str,
    limit: Union[Unset, int] = 5,
) -> Optional[Union[HTTPValidationError, list["SearchbarItemDTO"]]]:
    """Get Searchbar Suggestion

     Get search suggestions for a given query.

    This endpoint provides search suggestions based on the query string. The results are filtered and
    sorted.

    Args:
    - **q**: The search query to get suggestions for.
    - **limit**: The maximum number of suggestions to return, default is 5.

    Returns:
    - **list[SearchbarItemDTO]**: A list of search suggestion items.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if no data matching the search query is found.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        q (str):
        limit (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SearchbarItemDTO']]
    """

    return sync_detailed(
        client=client,
        q=q,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    q: str,
    limit: Union[Unset, int] = 5,
) -> Response[Union[HTTPValidationError, list["SearchbarItemDTO"]]]:
    """Get Searchbar Suggestion

     Get search suggestions for a given query.

    This endpoint provides search suggestions based on the query string. The results are filtered and
    sorted.

    Args:
    - **q**: The search query to get suggestions for.
    - **limit**: The maximum number of suggestions to return, default is 5.

    Returns:
    - **list[SearchbarItemDTO]**: A list of search suggestion items.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if no data matching the search query is found.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        q (str):
        limit (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SearchbarItemDTO']]]
    """

    kwargs = _get_kwargs(
        q=q,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    q: str,
    limit: Union[Unset, int] = 5,
) -> Optional[Union[HTTPValidationError, list["SearchbarItemDTO"]]]:
    """Get Searchbar Suggestion

     Get search suggestions for a given query.

    This endpoint provides search suggestions based on the query string. The results are filtered and
    sorted.

    Args:
    - **q**: The search query to get suggestions for.
    - **limit**: The maximum number of suggestions to return, default is 5.

    Returns:
    - **list[SearchbarItemDTO]**: A list of search suggestion items.

    Raises:
    - **404 Not Found (ObjectNotFound)**: Raised if no data matching the search query is found.
    - **500 Internal Server Error (DBConnectionException)**: Raised if a database connection error
    occurs.

    Args:
        q (str):
        limit (Union[Unset, int]):  Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SearchbarItemDTO']]
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            limit=limit,
        )
    ).parsed
