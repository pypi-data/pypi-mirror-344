from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.document_type import DocumentType
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_union_subreddit_info_schema_youtube_channel_info_schema_article_schema_reddit_post_schema_document_reddit_comment_schema_youtube_video_schema_youtube_comment_schema import (
    PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    document_type: DocumentType,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_document_type = document_type.value
    params["document_type"] = json_document_type

    params["page"] = page

    params["per_page"] = per_page

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/documents",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
    ]
]:
    if response.status_code == 200:
        response_200 = PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema.from_dict(
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
    Union[
        HTTPValidationError,
        PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    document_type: DocumentType,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[
    Union[
        HTTPValidationError,
        PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
    ]
]:
    """Get Documents By Type

     Get a paginated list of documents by type.

    This endpoint returns a paginated list of documents filtered by the specified document type.

    Args:
    - **document_type**: The type of document to filter by.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[DocumentTypesDTO]**: A paginated response containing documents of the
    specified type.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents of the specified type are found.

    Args:
        document_type (DocumentType): Enumeration class representing document types.

            Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                REDDIT_COMMENT: Represents reddit comment document.
                YOUTUBE_VIDEO: Represents youtube video document
                YOUTUBE_COMMENT: Represents youtube comment document
                YOUTUBE_CHANNEL_INFO: Represents youtube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema]]
    """

    kwargs = _get_kwargs(
        document_type=document_type,
        page=page,
        per_page=per_page,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    document_type: DocumentType,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[
    Union[
        HTTPValidationError,
        PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
    ]
]:
    """Get Documents By Type

     Get a paginated list of documents by type.

    This endpoint returns a paginated list of documents filtered by the specified document type.

    Args:
    - **document_type**: The type of document to filter by.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[DocumentTypesDTO]**: A paginated response containing documents of the
    specified type.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents of the specified type are found.

    Args:
        document_type (DocumentType): Enumeration class representing document types.

            Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                REDDIT_COMMENT: Represents reddit comment document.
                YOUTUBE_VIDEO: Represents youtube video document
                YOUTUBE_COMMENT: Represents youtube comment document
                YOUTUBE_CHANNEL_INFO: Represents youtube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema]
    """

    return sync_detailed(
        client=client,
        document_type=document_type,
        page=page,
        per_page=per_page,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    document_type: DocumentType,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Response[
    Union[
        HTTPValidationError,
        PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
    ]
]:
    """Get Documents By Type

     Get a paginated list of documents by type.

    This endpoint returns a paginated list of documents filtered by the specified document type.

    Args:
    - **document_type**: The type of document to filter by.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[DocumentTypesDTO]**: A paginated response containing documents of the
    specified type.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents of the specified type are found.

    Args:
        document_type (DocumentType): Enumeration class representing document types.

            Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                REDDIT_COMMENT: Represents reddit comment document.
                YOUTUBE_VIDEO: Represents youtube video document
                YOUTUBE_COMMENT: Represents youtube comment document
                YOUTUBE_CHANNEL_INFO: Represents youtube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema]]
    """

    kwargs = _get_kwargs(
        document_type=document_type,
        page=page,
        per_page=per_page,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    document_type: DocumentType,
    page: Union[Unset, int] = 1,
    per_page: Union[Unset, int] = 10,
) -> Optional[
    Union[
        HTTPValidationError,
        PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema,
    ]
]:
    """Get Documents By Type

     Get a paginated list of documents by type.

    This endpoint returns a paginated list of documents filtered by the specified document type.

    Args:
    - **document_type**: The type of document to filter by.
    - **page**: The page number for pagination, default is 1.
    - **per_page**: The number of items per page, default is 10, with a maximum of 100.

    Returns:
    - **PaginatedResponse[DocumentTypesDTO]**: A paginated response containing documents of the
    specified type.

    Raises:
    - **404 Not Found (DocumentsNotFound)**: Raised if no documents of the specified type are found.

    Args:
        document_type (DocumentType): Enumeration class representing document types.

            Attributes:
                ARTICLE: Represents news article document.
                REDDIT_POST: Represents reddit post document.
                REDDIT_COMMENT: Represents reddit comment document.
                YOUTUBE_VIDEO: Represents youtube video document
                YOUTUBE_COMMENT: Represents youtube comment document
                YOUTUBE_CHANNEL_INFO: Represents youtube channel info document
                SUBREDDIT_INFO: Represents subreddit info document
        page (Union[Unset, int]):  Default: 1.
        per_page (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            document_type=document_type,
            page=page,
            per_page=per_page,
        )
    ).parsed
