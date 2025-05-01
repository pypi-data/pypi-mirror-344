from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_schema import PromptSchema
from ...models.response_with_metadata_schema_prompt_info_schema import ResponseWithMetadataSchemaPromptInfoSchema
from ...types import Response


def _get_kwargs(
    *,
    body: PromptSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/prompts",
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
    *,
    client: AuthenticatedClient,
    body: PromptSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Create Prompt

     Create a new prompt.

    This endpoint allows superusers or moderators to create a new prompt.

    Args:
    - **prompt_data[PromptSchema]**: Schema containing the prompt details.

    Returns:
    - **PromptInfoSchema**: The details of the newly created prompt.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **422 Unprocessable entity (InvalidPromptInputDataException)**: Raised if the input data for the
    prompt is invalid.

    Args:
        body (PromptSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: PromptSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Create Prompt

     Create a new prompt.

    This endpoint allows superusers or moderators to create a new prompt.

    Args:
    - **prompt_data[PromptSchema]**: Schema containing the prompt details.

    Returns:
    - **PromptInfoSchema**: The details of the newly created prompt.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **422 Unprocessable entity (InvalidPromptInputDataException)**: Raised if the input data for the
    prompt is invalid.

    Args:
        body (PromptSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PromptSchema,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Create Prompt

     Create a new prompt.

    This endpoint allows superusers or moderators to create a new prompt.

    Args:
    - **prompt_data[PromptSchema]**: Schema containing the prompt details.

    Returns:
    - **PromptInfoSchema**: The details of the newly created prompt.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **422 Unprocessable entity (InvalidPromptInputDataException)**: Raised if the input data for the
    prompt is invalid.

    Args:
        body (PromptSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PromptSchema,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]]:
    """Create Prompt

     Create a new prompt.

    This endpoint allows superusers or moderators to create a new prompt.

    Args:
    - **prompt_data[PromptSchema]**: Schema containing the prompt details.

    Returns:
    - **PromptInfoSchema**: The details of the newly created prompt.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.
    - **422 Unprocessable entity (InvalidPromptInputDataException)**: Raised if the input data for the
    prompt is invalid.

    Args:
        body (PromptSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptInfoSchema]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
