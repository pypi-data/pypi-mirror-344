from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_type import PromptType
from ...models.response_with_metadata_schema_prompt_params_info_schema import (
    ResponseWithMetadataSchemaPromptParamsInfoSchema,
)
from ...types import Response


def _get_kwargs(
    prompt_type: PromptType,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/prompts/params/{prompt_type}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemaPromptParamsInfoSchema.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    prompt_type: PromptType,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]:
    """Get Prompt Params Info

     Retrieve input and output parameters for a specific prompt type.

    This endpoint allows superusers or moderators to fetch the parameter details of a specific prompt
    type.

    Args:
    - **prompt_type[PromptType]**: The type of the prompt to retrieve parameters for.

    Returns:
    - **PromptParamsInfoSchema**: The input and output parameter details for the specified prompt type.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_type=prompt_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    prompt_type: PromptType,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]:
    """Get Prompt Params Info

     Retrieve input and output parameters for a specific prompt type.

    This endpoint allows superusers or moderators to fetch the parameter details of a specific prompt
    type.

    Args:
    - **prompt_type[PromptType]**: The type of the prompt to retrieve parameters for.

    Returns:
    - **PromptParamsInfoSchema**: The input and output parameter details for the specified prompt type.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]
    """

    return sync_detailed(
        prompt_type=prompt_type,
        client=client,
    ).parsed


async def asyncio_detailed(
    prompt_type: PromptType,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]:
    """Get Prompt Params Info

     Retrieve input and output parameters for a specific prompt type.

    This endpoint allows superusers or moderators to fetch the parameter details of a specific prompt
    type.

    Args:
    - **prompt_type[PromptType]**: The type of the prompt to retrieve parameters for.

    Returns:
    - **PromptParamsInfoSchema**: The input and output parameter details for the specified prompt type.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]
    """

    kwargs = _get_kwargs(
        prompt_type=prompt_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    prompt_type: PromptType,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]]:
    """Get Prompt Params Info

     Retrieve input and output parameters for a specific prompt type.

    This endpoint allows superusers or moderators to fetch the parameter details of a specific prompt
    type.

    Args:
    - **prompt_type[PromptType]**: The type of the prompt to retrieve parameters for.

    Returns:
    - **PromptParamsInfoSchema**: The input and output parameter details for the specified prompt type.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not a superuser or moderator.

    Args:
        prompt_type (PromptType): Enumeration class representing prompt types.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemaPromptParamsInfoSchema]
    """

    return (
        await asyncio_detailed(
            prompt_type=prompt_type,
            client=client,
        )
    ).parsed
