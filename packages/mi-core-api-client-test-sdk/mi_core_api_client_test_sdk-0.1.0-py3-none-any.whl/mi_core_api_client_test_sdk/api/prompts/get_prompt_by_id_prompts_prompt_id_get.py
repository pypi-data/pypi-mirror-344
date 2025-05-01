from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schema_prompt_info_schema import ResponseWithMetadataSchemaPromptInfoSchema
from ...types import Response


def _get_kwargs(
    prompt_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/prompts/{prompt_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPromptInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Get Prompt By Id

     Retrieve a prompt by its ID.

    This endpoint allows superusers or moderators to fetch the details of a specific prompt by its ID.

    Args:
    - **prompt_id**: The ID of the prompt to retrieve.

    Returns:
    - **PromptInfoSchema**: The details of the requested prompt.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **400 Bad request (InvalidPromptTypeException)**: Raised if the prompt type does not match the
    expected type.

    Args:
        prompt_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_id=prompt_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Get Prompt By Id

     Retrieve a prompt by its ID.

    This endpoint allows superusers or moderators to fetch the details of a specific prompt by its ID.

    Args:
    - **prompt_id**: The ID of the prompt to retrieve.

    Returns:
    - **PromptInfoSchema**: The details of the requested prompt.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **400 Bad request (InvalidPromptTypeException)**: Raised if the prompt type does not match the
    expected type.

    Args:
        prompt_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]
    """

    return sync_detailed(
        prompt_id=prompt_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Get Prompt By Id

     Retrieve a prompt by its ID.

    This endpoint allows superusers or moderators to fetch the details of a specific prompt by its ID.

    Args:
    - **prompt_id**: The ID of the prompt to retrieve.

    Returns:
    - **PromptInfoSchema**: The details of the requested prompt.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **400 Bad request (InvalidPromptTypeException)**: Raised if the prompt type does not match the
    expected type.

    Args:
        prompt_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_id=prompt_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Get Prompt By Id

     Retrieve a prompt by its ID.

    This endpoint allows superusers or moderators to fetch the details of a specific prompt by its ID.

    Args:
    - **prompt_id**: The ID of the prompt to retrieve.

    Returns:
    - **PromptInfoSchema**: The details of the requested prompt.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **400 Bad request (InvalidPromptTypeException)**: Raised if the prompt type does not match the
    expected type.

    Args:
        prompt_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]
    """

    return (
        await asyncio_detailed(
            prompt_id=prompt_id,
            client=client,
        )
    ).parsed
