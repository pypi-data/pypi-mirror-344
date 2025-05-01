import datetime
from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx
from dateutil.parser import isoparse

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.metric import Metric
from ...models.observed_document_type import ObservedDocumentType
from ...models.response_with_metadata_schema_document_metrics_dto import ResponseWithMetadataSchemaDocumentMetricsDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    document_id: UUID,
    metric: Metric,
    document_type: ObservedDocumentType,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:13.983245"),
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_document_id = str(document_id)
    params["document_id"] = json_document_id

    json_metric = metric.value
    params["metric"] = json_metric

    json_document_type = document_type.value
    params["document_type"] = json_document_type

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["start_date"] = json_start_date

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["end_date"] = json_end_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/bigquery/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaDocumentMetricsDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    document_id: UUID,
    metric: Metric,
    document_type: ObservedDocumentType,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:13.983245"),
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]:
    """Get Metrics By Document Id

    Args:
        document_id (UUID):
        metric (Metric): Enumeration class representing metrics.

            Attributes:
                UPVOTES: Represents upvotes metric.
                COMMENTS_COUNT: Represents comments count metric.
                VIEWS: Represents views metric.
                LIKES: Represents likes metric.
                SUBSCRIBERS: Represents subscribers metric.
                TOTAL_VIEWS: Represents total views metric.
                ONLINE_MEMBERS: Represents online members metric.
                MEMBERS: Represents members metric.
                RANK: Represents rank metric.
                BODY: Represents body metric.
                TITLE: Represents title metric.
                EST_REV : Represents estimated revenue metric.
                TOTAL_VIDEOS: Represents total videos metric.
                POSTS_COUNT: Represents posts count metric.
                POSTS_COMMENTS_COUNT: Represents posts comments count metric.
                POSTS_UPVOTES: Represents posts upvotes metric.
        document_type (ObservedDocumentType): Enumeration class representing observed document
            types.

                Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                YOUTUBE_VIDEO: Represents YouTube video document
                YOUTUBE_CHANNEL_INFO: Represents YouTube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:13.983245').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        metric=metric,
        document_type=document_type,
        start_date=start_date,
        end_date=end_date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    document_id: UUID,
    metric: Metric,
    document_type: ObservedDocumentType,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:13.983245"),
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]:
    """Get Metrics By Document Id

    Args:
        document_id (UUID):
        metric (Metric): Enumeration class representing metrics.

            Attributes:
                UPVOTES: Represents upvotes metric.
                COMMENTS_COUNT: Represents comments count metric.
                VIEWS: Represents views metric.
                LIKES: Represents likes metric.
                SUBSCRIBERS: Represents subscribers metric.
                TOTAL_VIEWS: Represents total views metric.
                ONLINE_MEMBERS: Represents online members metric.
                MEMBERS: Represents members metric.
                RANK: Represents rank metric.
                BODY: Represents body metric.
                TITLE: Represents title metric.
                EST_REV : Represents estimated revenue metric.
                TOTAL_VIDEOS: Represents total videos metric.
                POSTS_COUNT: Represents posts count metric.
                POSTS_COMMENTS_COUNT: Represents posts comments count metric.
                POSTS_UPVOTES: Represents posts upvotes metric.
        document_type (ObservedDocumentType): Enumeration class representing observed document
            types.

                Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                YOUTUBE_VIDEO: Represents YouTube video document
                YOUTUBE_CHANNEL_INFO: Represents YouTube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:13.983245').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]
    """

    return sync_detailed(
        client=client,
        document_id=document_id,
        metric=metric,
        document_type=document_type,
        start_date=start_date,
        end_date=end_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    document_id: UUID,
    metric: Metric,
    document_type: ObservedDocumentType,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:13.983245"),
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]:
    """Get Metrics By Document Id

    Args:
        document_id (UUID):
        metric (Metric): Enumeration class representing metrics.

            Attributes:
                UPVOTES: Represents upvotes metric.
                COMMENTS_COUNT: Represents comments count metric.
                VIEWS: Represents views metric.
                LIKES: Represents likes metric.
                SUBSCRIBERS: Represents subscribers metric.
                TOTAL_VIEWS: Represents total views metric.
                ONLINE_MEMBERS: Represents online members metric.
                MEMBERS: Represents members metric.
                RANK: Represents rank metric.
                BODY: Represents body metric.
                TITLE: Represents title metric.
                EST_REV : Represents estimated revenue metric.
                TOTAL_VIDEOS: Represents total videos metric.
                POSTS_COUNT: Represents posts count metric.
                POSTS_COMMENTS_COUNT: Represents posts comments count metric.
                POSTS_UPVOTES: Represents posts upvotes metric.
        document_type (ObservedDocumentType): Enumeration class representing observed document
            types.

                Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                YOUTUBE_VIDEO: Represents YouTube video document
                YOUTUBE_CHANNEL_INFO: Represents YouTube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:13.983245').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
        metric=metric,
        document_type=document_type,
        start_date=start_date,
        end_date=end_date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    document_id: UUID,
    metric: Metric,
    document_type: ObservedDocumentType,
    start_date: Union[Unset, datetime.datetime] = isoparse("1970-01-01T00:00:00"),
    end_date: Union[Unset, datetime.datetime] = isoparse("2025-05-01T09:12:13.983245"),
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]]:
    """Get Metrics By Document Id

    Args:
        document_id (UUID):
        metric (Metric): Enumeration class representing metrics.

            Attributes:
                UPVOTES: Represents upvotes metric.
                COMMENTS_COUNT: Represents comments count metric.
                VIEWS: Represents views metric.
                LIKES: Represents likes metric.
                SUBSCRIBERS: Represents subscribers metric.
                TOTAL_VIEWS: Represents total views metric.
                ONLINE_MEMBERS: Represents online members metric.
                MEMBERS: Represents members metric.
                RANK: Represents rank metric.
                BODY: Represents body metric.
                TITLE: Represents title metric.
                EST_REV : Represents estimated revenue metric.
                TOTAL_VIDEOS: Represents total videos metric.
                POSTS_COUNT: Represents posts count metric.
                POSTS_COMMENTS_COUNT: Represents posts comments count metric.
                POSTS_UPVOTES: Represents posts upvotes metric.
        document_type (ObservedDocumentType): Enumeration class representing observed document
            types.

                Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                YOUTUBE_VIDEO: Represents YouTube video document
                YOUTUBE_CHANNEL_INFO: Represents YouTube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        start_date (Union[Unset, datetime.datetime]):  Default: isoparse('1970-01-01T00:00:00').
        end_date (Union[Unset, datetime.datetime]):  Default:
            isoparse('2025-05-01T09:12:13.983245').

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaDocumentMetricsDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            document_id=document_id,
            metric=metric,
            document_type=document_type,
            start_date=start_date,
            end_date=end_date,
        )
    ).parsed
