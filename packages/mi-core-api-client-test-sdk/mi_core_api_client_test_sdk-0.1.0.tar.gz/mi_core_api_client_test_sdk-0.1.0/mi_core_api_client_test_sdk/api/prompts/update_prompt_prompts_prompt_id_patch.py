from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_update_schema import PromptUpdateSchema
from ...models.response_with_metadata_schema_prompt_info_schema import ResponseWithMetadataSchemaPromptInfoSchema
from ...types import Response


def _get_kwargs(
    prompt_id: UUID,
    *,
    body: PromptUpdateSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/prompts/{prompt_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: PromptUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Update Prompt

     Update an existing prompt.

    This endpoint allows superusers or moderators to update the details of a specific prompt.

    Args:
    - **prompt_id**: The ID of the prompt to update.
    - **data[PromptUpdateSchema]**: Schema containing the updated prompt details.
    Returns:
    - **PromptInfoSchema**: The updated prompt details.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_id (UUID):
        body (PromptUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_id=prompt_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
    body: PromptUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Update Prompt

     Update an existing prompt.

    This endpoint allows superusers or moderators to update the details of a specific prompt.

    Args:
    - **prompt_id**: The ID of the prompt to update.
    - **data[PromptUpdateSchema]**: Schema containing the updated prompt details.
    Returns:
    - **PromptInfoSchema**: The updated prompt details.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_id (UUID):
        body (PromptUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]
    """

    return sync_detailed(
        prompt_id=prompt_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
    body: PromptUpdateSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Update Prompt

     Update an existing prompt.

    This endpoint allows superusers or moderators to update the details of a specific prompt.

    Args:
    - **prompt_id**: The ID of the prompt to update.
    - **data[PromptUpdateSchema]**: Schema containing the updated prompt details.
    Returns:
    - **PromptInfoSchema**: The updated prompt details.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_id (UUID):
        body (PromptUpdateSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_id=prompt_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    prompt_id: UUID,
    *,
    client: AuthenticatedClient,
    body: PromptUpdateSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Update Prompt

     Update an existing prompt.

    This endpoint allows superusers or moderators to update the details of a specific prompt.

    Args:
    - **prompt_id**: The ID of the prompt to update.
    - **data[PromptUpdateSchema]**: Schema containing the updated prompt details.
    Returns:
    - **PromptInfoSchema**: The updated prompt details.

    Raises:
    - **404 Not Found (PromptNotFound)**: Raised if the prompt with the given ID does not exist.
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_id (UUID):
        body (PromptUpdateSchema):

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
            body=body,
        )
    ).parsed
