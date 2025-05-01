from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: UUID,
    *,
    custom_field_ids: Union[Unset, list[UUID]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_custom_field_ids: Union[Unset, list[str]] = UNSET
    if not isinstance(custom_field_ids, Unset):
        json_custom_field_ids = []
        for custom_field_ids_item_data in custom_field_ids:
            custom_field_ids_item = str(custom_field_ids_item_data)
            json_custom_field_ids.append(custom_field_ids_item)

    params["custom_field_ids"] = json_custom_field_ids

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/custom-fields/{project_id}/llm/values",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    custom_field_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Generate Values For Custom Fields By Project

     Generate values for custom fields within the specified project using an LLM.

    This endpoint triggers background processing of custom fields of type **apply_prompt** or
    **validated_prompt**
    to generate and store values for associated documents. If custom_field_ids are provided, only those
    fields
    are processed. Otherwise, all eligible custom fields in the project are processed.
    Fields of type **data_lookup** are not supported and will be skipped or cause an error if explicitly
    provided.

    Args:
    - **project_id**: ID of the project to process custom fields for.
    - **custom_field_ids**: (Optional) List of custom field IDs to process. If empty, all eligible
    fields in the project will be processed.

    Returns:
    - **200 Ok**:  A successful response with no content.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.
    - **404 Not Found (CustomFieldNotFound)**: Raised if project does not contain custom field records
    with permitted type or there was no data found based on the provided custom field IDs.

    Args:
        project_id (UUID):
        custom_field_ids (Union[Unset, list[UUID]]): List of custom field IDs to update field
            values for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        custom_field_ids=custom_field_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    custom_field_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Generate Values For Custom Fields By Project

     Generate values for custom fields within the specified project using an LLM.

    This endpoint triggers background processing of custom fields of type **apply_prompt** or
    **validated_prompt**
    to generate and store values for associated documents. If custom_field_ids are provided, only those
    fields
    are processed. Otherwise, all eligible custom fields in the project are processed.
    Fields of type **data_lookup** are not supported and will be skipped or cause an error if explicitly
    provided.

    Args:
    - **project_id**: ID of the project to process custom fields for.
    - **custom_field_ids**: (Optional) List of custom field IDs to process. If empty, all eligible
    fields in the project will be processed.

    Returns:
    - **200 Ok**:  A successful response with no content.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.
    - **404 Not Found (CustomFieldNotFound)**: Raised if project does not contain custom field records
    with permitted type or there was no data found based on the provided custom field IDs.

    Args:
        project_id (UUID):
        custom_field_ids (Union[Unset, list[UUID]]): List of custom field IDs to update field
            values for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        custom_field_ids=custom_field_ids,
    ).parsed


async def asyncio_detailed(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    custom_field_ids: Union[Unset, list[UUID]] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Generate Values For Custom Fields By Project

     Generate values for custom fields within the specified project using an LLM.

    This endpoint triggers background processing of custom fields of type **apply_prompt** or
    **validated_prompt**
    to generate and store values for associated documents. If custom_field_ids are provided, only those
    fields
    are processed. Otherwise, all eligible custom fields in the project are processed.
    Fields of type **data_lookup** are not supported and will be skipped or cause an error if explicitly
    provided.

    Args:
    - **project_id**: ID of the project to process custom fields for.
    - **custom_field_ids**: (Optional) List of custom field IDs to process. If empty, all eligible
    fields in the project will be processed.

    Returns:
    - **200 Ok**:  A successful response with no content.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.
    - **404 Not Found (CustomFieldNotFound)**: Raised if project does not contain custom field records
    with permitted type or there was no data found based on the provided custom field IDs.

    Args:
        project_id (UUID):
        custom_field_ids (Union[Unset, list[UUID]]): List of custom field IDs to update field
            values for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        custom_field_ids=custom_field_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: UUID,
    *,
    client: AuthenticatedClient,
    custom_field_ids: Union[Unset, list[UUID]] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Generate Values For Custom Fields By Project

     Generate values for custom fields within the specified project using an LLM.

    This endpoint triggers background processing of custom fields of type **apply_prompt** or
    **validated_prompt**
    to generate and store values for associated documents. If custom_field_ids are provided, only those
    fields
    are processed. Otherwise, all eligible custom fields in the project are processed.
    Fields of type **data_lookup** are not supported and will be skipped or cause an error if explicitly
    provided.

    Args:
    - **project_id**: ID of the project to process custom fields for.
    - **custom_field_ids**: (Optional) List of custom field IDs to process. If empty, all eligible
    fields in the project will be processed.

    Returns:
    - **200 Ok**:  A successful response with no content.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.
    - **404 Not Found (ProjectNotFound)**: Raised if no project is found based on the provided ID.
    - **404 Not Found (CustomFieldNotFound)**: Raised if project does not contain custom field records
    with permitted type or there was no data found based on the provided custom field IDs.

    Args:
        project_id (UUID):
        custom_field_ids (Union[Unset, list[UUID]]): List of custom field IDs to update field
            values for

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            custom_field_ids=custom_field_ids,
        )
    ).parsed
