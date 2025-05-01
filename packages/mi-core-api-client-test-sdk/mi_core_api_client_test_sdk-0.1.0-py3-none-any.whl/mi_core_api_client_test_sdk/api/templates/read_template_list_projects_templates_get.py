from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_with_metadata_schemalist_template_dto import ResponseWithMetadataSchemalistTemplateDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    template_name: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_template_name: Union[None, Unset, str]
    if isinstance(template_name, Unset):
        json_template_name = UNSET
    else:
        json_template_name = template_name
    params["template_name"] = json_template_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/templates",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]:
    if response.status_code == 200:
        response_200 = ResponseWithMetadataSchemalistTemplateDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    template_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]:
    """Read Template List

     Get a list of saved templates for the current user.

    Args:
    - **template_name**: (Optional) Filter templates by name.

    Returns:
    - **list[TemplateDTO]**: List of available templates.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        template_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]
    """

    kwargs = _get_kwargs(
        template_name=template_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    template_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]:
    """Read Template List

     Get a list of saved templates for the current user.

    Args:
    - **template_name**: (Optional) Filter templates by name.

    Returns:
    - **list[TemplateDTO]**: List of available templates.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        template_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]
    """

    return sync_detailed(
        client=client,
        template_name=template_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    template_name: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]:
    """Read Template List

     Get a list of saved templates for the current user.

    Args:
    - **template_name**: (Optional) Filter templates by name.

    Returns:
    - **list[TemplateDTO]**: List of available templates.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        template_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]
    """

    kwargs = _get_kwargs(
        template_name=template_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    template_name: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]]:
    """Read Template List

     Get a list of saved templates for the current user.

    Args:
    - **template_name**: (Optional) Filter templates by name.

    Returns:
    - **list[TemplateDTO]**: List of available templates.

    Raises:
    - **401 Unauthorized (CredentialException)**: Raised if the user is not found in Firebase.
    - **401 Unauthorized (PermissionException)**: Raised if the API key is invalid, expired or no valid
    key or bearer token was provided.
    - **403 Forbidden (UserNotAuthenticated)**: Raised if user ID could not be extracted from the token.

    Args:
        template_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ResponseWithMetadataSchemalistTemplateDTO]
    """

    return (
        await asyncio_detailed(
            client=client,
            template_name=template_name,
        )
    ).parsed
