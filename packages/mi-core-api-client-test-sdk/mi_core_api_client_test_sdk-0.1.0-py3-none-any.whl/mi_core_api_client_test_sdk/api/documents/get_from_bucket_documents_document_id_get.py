from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.subreddit_response_row import SubredditResponseRow
from ...models.yt_response_row import YTResponseRow
from ...types import Response


def _get_kwargs(
    document_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/documents/{document_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Union["SubredditResponseRow", "YTResponseRow"]]]:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> Union["SubredditResponseRow", "YTResponseRow"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = YTResponseRow.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = SubredditResponseRow.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

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
) -> Response[Union[HTTPValidationError, Union["SubredditResponseRow", "YTResponseRow"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    document_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, Union["SubredditResponseRow", "YTResponseRow"]]]:
    """Get From Bucket

     Get document from the storage bucket.

    This endpoint retrieves a document from the bucket based on the document ID.

    Args:
    - **document_id**: The unique identifier of the document to retrieve.

    Returns:
    - **YTResponseRow | SubredditResponseRow**: The retrieved document, which can be a YouTube or
    Subreddit response.

    Raises:
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.

    Args:
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['SubredditResponseRow', 'YTResponseRow']]]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    document_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, Union["SubredditResponseRow", "YTResponseRow"]]]:
    """Get From Bucket

     Get document from the storage bucket.

    This endpoint retrieves a document from the bucket based on the document ID.

    Args:
    - **document_id**: The unique identifier of the document to retrieve.

    Returns:
    - **YTResponseRow | SubredditResponseRow**: The retrieved document, which can be a YouTube or
    Subreddit response.

    Raises:
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.

    Args:
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['SubredditResponseRow', 'YTResponseRow']]
    """

    return sync_detailed(
        document_id=document_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    document_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[HTTPValidationError, Union["SubredditResponseRow", "YTResponseRow"]]]:
    """Get From Bucket

     Get document from the storage bucket.

    This endpoint retrieves a document from the bucket based on the document ID.

    Args:
    - **document_id**: The unique identifier of the document to retrieve.

    Returns:
    - **YTResponseRow | SubredditResponseRow**: The retrieved document, which can be a YouTube or
    Subreddit response.

    Raises:
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.

    Args:
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['SubredditResponseRow', 'YTResponseRow']]]
    """

    kwargs = _get_kwargs(
        document_id=document_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    document_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[HTTPValidationError, Union["SubredditResponseRow", "YTResponseRow"]]]:
    """Get From Bucket

     Get document from the storage bucket.

    This endpoint retrieves a document from the bucket based on the document ID.

    Args:
    - **document_id**: The unique identifier of the document to retrieve.

    Returns:
    - **YTResponseRow | SubredditResponseRow**: The retrieved document, which can be a YouTube or
    Subreddit response.

    Raises:
    - **404 Not Found (BucketFileNotFoundException)**: Raised if the document with the given ID is not
    found in the bucket.

    Args:
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['SubredditResponseRow', 'YTResponseRow']]
    """

    return (
        await asyncio_detailed(
            document_id=document_id,
            client=client,
        )
    ).parsed
