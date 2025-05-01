from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemadictstr_list_union_google_raw_serp_result_dto_youtube_raw_serp_result_dto import (
    ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO,
)
from ...models.serp_search_engine import SerpSearchEngine
from ...models.youtube_search_content_type import YoutubeSearchContentType
from ...models.youtube_search_duration import YoutubeSearchDuration
from ...models.youtube_search_sort_by import YoutubeSearchSortBy
from ...models.youtube_search_upload_date import YoutubeSearchUploadDate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    queries: list[str],
    total_posts: Union[Unset, int] = 5,
    upload_date: Union[Unset, YoutubeSearchUploadDate] = UNSET,
    content_type: Union[Unset, YoutubeSearchContentType] = UNSET,
    duration: Union[Unset, YoutubeSearchDuration] = UNSET,
    sort_by: Union[Unset, YoutubeSearchSortBy] = UNSET,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
    start_date: Union[None, Unset, str] = UNSET,
    end_date: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_queries = queries

    params["queries"] = json_queries

    params["total_posts"] = total_posts

    json_upload_date: Union[Unset, str] = UNSET
    if not isinstance(upload_date, Unset):
        json_upload_date = upload_date.value

    params["upload_date"] = json_upload_date

    json_content_type: Union[Unset, str] = UNSET
    if not isinstance(content_type, Unset):
        json_content_type = content_type.value

    params["content_type"] = json_content_type

    json_duration: Union[Unset, str] = UNSET
    if not isinstance(duration, Unset):
        json_duration = duration.value

    params["duration"] = json_duration

    json_sort_by: Union[Unset, str] = UNSET
    if not isinstance(sort_by, Unset):
        json_sort_by = sort_by.value

    params["sort_by"] = json_sort_by

    json_engine: Union[Unset, str] = UNSET
    if not isinstance(engine, Unset):
        json_engine = engine.value

    params["engine"] = json_engine

    json_start_date: Union[None, Unset, str]
    if isinstance(start_date, Unset):
        json_start_date = UNSET
    else:
        json_start_date = start_date
    params["start_date"] = json_start_date

    json_end_date: Union[None, Unset, str]
    if isinstance(end_date, Unset):
        json_end_date = UNSET
    else:
        json_end_date = end_date
    params["end_date"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/youtube/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
]:
    if response.status_code == 200:
        response_200 = (
            ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO.from_dict(
                response.json()
            )
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
    Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
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
    queries: list[str],
    total_posts: Union[Unset, int] = 5,
    upload_date: Union[Unset, YoutubeSearchUploadDate] = UNSET,
    content_type: Union[Unset, YoutubeSearchContentType] = UNSET,
    duration: Union[Unset, YoutubeSearchDuration] = UNSET,
    sort_by: Union[Unset, YoutubeSearchSortBy] = UNSET,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
    start_date: Union[None, Unset, str] = UNSET,
    end_date: Union[None, Unset, str] = UNSET,
) -> Response[
    Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
]:
    """Get Search Results By Queries

     Get raw search results from SERP API for both Google and YouTube engines

    Args:
        queries (list[str]):
        total_posts (Union[Unset, int]):  Default: 5.
        upload_date (Union[Unset, YoutubeSearchUploadDate]): Enumeration class representing
            YouTube search upload date filters.
        content_type (Union[Unset, YoutubeSearchContentType]): Enumeration class representing
            YouTube search content type filters.
        duration (Union[Unset, YoutubeSearchDuration]): YouTube duration search filter: short (<
            4min), medium (4-20min), long (> 20min)
        sort_by (Union[Unset, YoutubeSearchSortBy]): Enumeration class representing YouTube search
            sort options.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.
        start_date (Union[None, Unset, str]): Start date for filtering results (format: YYYY-MM-
            DD)
        end_date (Union[None, Unset, str]): End date for filtering results (format: YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        total_posts=total_posts,
        upload_date=upload_date,
        content_type=content_type,
        duration=duration,
        sort_by=sort_by,
        engine=engine,
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    total_posts: Union[Unset, int] = 5,
    upload_date: Union[Unset, YoutubeSearchUploadDate] = UNSET,
    content_type: Union[Unset, YoutubeSearchContentType] = UNSET,
    duration: Union[Unset, YoutubeSearchDuration] = UNSET,
    sort_by: Union[Unset, YoutubeSearchSortBy] = UNSET,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
    start_date: Union[None, Unset, str] = UNSET,
    end_date: Union[None, Unset, str] = UNSET,
) -> Optional[
    Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
]:
    """Get Search Results By Queries

     Get raw search results from SERP API for both Google and YouTube engines

    Args:
        queries (list[str]):
        total_posts (Union[Unset, int]):  Default: 5.
        upload_date (Union[Unset, YoutubeSearchUploadDate]): Enumeration class representing
            YouTube search upload date filters.
        content_type (Union[Unset, YoutubeSearchContentType]): Enumeration class representing
            YouTube search content type filters.
        duration (Union[Unset, YoutubeSearchDuration]): YouTube duration search filter: short (<
            4min), medium (4-20min), long (> 20min)
        sort_by (Union[Unset, YoutubeSearchSortBy]): Enumeration class representing YouTube search
            sort options.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.
        start_date (Union[None, Unset, str]): Start date for filtering results (format: YYYY-MM-
            DD)
        end_date (Union[None, Unset, str]): End date for filtering results (format: YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
    """

    return sync_detailed(
        client=client,
        queries=queries,
        total_posts=total_posts,
        upload_date=upload_date,
        content_type=content_type,
        duration=duration,
        sort_by=sort_by,
        engine=engine,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    total_posts: Union[Unset, int] = 5,
    upload_date: Union[Unset, YoutubeSearchUploadDate] = UNSET,
    content_type: Union[Unset, YoutubeSearchContentType] = UNSET,
    duration: Union[Unset, YoutubeSearchDuration] = UNSET,
    sort_by: Union[Unset, YoutubeSearchSortBy] = UNSET,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
    start_date: Union[None, Unset, str] = UNSET,
    end_date: Union[None, Unset, str] = UNSET,
) -> Response[
    Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
]:
    """Get Search Results By Queries

     Get raw search results from SERP API for both Google and YouTube engines

    Args:
        queries (list[str]):
        total_posts (Union[Unset, int]):  Default: 5.
        upload_date (Union[Unset, YoutubeSearchUploadDate]): Enumeration class representing
            YouTube search upload date filters.
        content_type (Union[Unset, YoutubeSearchContentType]): Enumeration class representing
            YouTube search content type filters.
        duration (Union[Unset, YoutubeSearchDuration]): YouTube duration search filter: short (<
            4min), medium (4-20min), long (> 20min)
        sort_by (Union[Unset, YoutubeSearchSortBy]): Enumeration class representing YouTube search
            sort options.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.
        start_date (Union[None, Unset, str]): Start date for filtering results (format: YYYY-MM-
            DD)
        end_date (Union[None, Unset, str]): End date for filtering results (format: YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]]
    """

    kwargs = _get_kwargs(
        queries=queries,
        total_posts=total_posts,
        upload_date=upload_date,
        content_type=content_type,
        duration=duration,
        sort_by=sort_by,
        engine=engine,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    queries: list[str],
    total_posts: Union[Unset, int] = 5,
    upload_date: Union[Unset, YoutubeSearchUploadDate] = UNSET,
    content_type: Union[Unset, YoutubeSearchContentType] = UNSET,
    duration: Union[Unset, YoutubeSearchDuration] = UNSET,
    sort_by: Union[Unset, YoutubeSearchSortBy] = UNSET,
    engine: Union[Unset, SerpSearchEngine] = UNSET,
    start_date: Union[None, Unset, str] = UNSET,
    end_date: Union[None, Unset, str] = UNSET,
) -> Optional[
    Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
]:
    """Get Search Results By Queries

     Get raw search results from SERP API for both Google and YouTube engines

    Args:
        queries (list[str]):
        total_posts (Union[Unset, int]):  Default: 5.
        upload_date (Union[Unset, YoutubeSearchUploadDate]): Enumeration class representing
            YouTube search upload date filters.
        content_type (Union[Unset, YoutubeSearchContentType]): Enumeration class representing
            YouTube search content type filters.
        duration (Union[Unset, YoutubeSearchDuration]): YouTube duration search filter: short (<
            4min), medium (4-20min), long (> 20min)
        sort_by (Union[Unset, YoutubeSearchSortBy]): Enumeration class representing YouTube search
            sort options.
        engine (Union[Unset, SerpSearchEngine]): Enumeration class representing SERP search
            engines.
        start_date (Union[None, Unset, str]): Start date for filtering results (format: YYYY-MM-
            DD)
        end_date (Union[None, Unset, str]): End date for filtering results (format: YYYY-MM-DD)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemadictstrListUnionGoogleRawSerpResultDTOYoutubeRawSerpResultDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            queries=queries,
            total_posts=total_posts,
            upload_date=upload_date,
            content_type=content_type,
            duration=duration,
            sort_by=sort_by,
            engine=engine,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
