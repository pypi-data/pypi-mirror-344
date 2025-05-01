from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.collect_storyboard_generation_params import CollectStoryboardGenerationParams
from ...models.http_validation_error import HTTPValidationError
from ...models.storyboard_generation_status_dto import StoryboardGenerationStatusDTO
from ...types import Response


def _get_kwargs(
    storyboard_id: UUID,
    *,
    body: CollectStoryboardGenerationParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/storyboards/{storyboard_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]:
    if response.status_code == 200:
        response_200 = StoryboardGenerationStatusDTO.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CollectStoryboardGenerationParams,
) -> Response[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]:
    """Regenerate Storyboard

     Regenerate a storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard to regenerate.
    - **scenario_generation_inputs[CollectStoryboardGenerationParams]**: Input parameters for storyboard
    regeneration.

    Returns:
    - **StoryboardGenerationStatusDTO**: The status of the storyboard regeneration process.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.

    Args:
        storyboard_id (UUID):
        body (CollectStoryboardGenerationParams):  Example: {'archetype_restriction':
            {'archetype_description': 'This format revolves around telling a personal or historical
            story in a compelling, narrative style. It focuses on building emotional connections
            through plot, characters, and personal experiences. Viewers are drawn in by the
            storytelling quality, relating to the journey or learning from past events.',
            'archetype_examples': ['How I Overcame My Fear of Public Speaking', 'The Untold Story
            Behind a 100-Year-Old Painting', 'My Experience Living in a Remote Village', 'Surviving a
            Near-Disaster: A Personal Account', 'A Grandmother’s Tale: Life Lessons from the 1950s'],
            'archetype_title': 'Storytelling Narrative'}, 'existing_content_summary': 'the pros and
            cons of different note-taking apps.', 'hard_restrictions': ['Duration < 5 minutes',
            'language = English', 'no profanity'], 'seed_keywords': ['handwriting to text goodnotes',
            'notability handwriting to text'], 'soft_restrictions': ['Use humor', 'feature dogs as
            characters']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]
    """

    kwargs = _get_kwargs(
        storyboard_id=storyboard_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CollectStoryboardGenerationParams,
) -> Optional[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]:
    """Regenerate Storyboard

     Regenerate a storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard to regenerate.
    - **scenario_generation_inputs[CollectStoryboardGenerationParams]**: Input parameters for storyboard
    regeneration.

    Returns:
    - **StoryboardGenerationStatusDTO**: The status of the storyboard regeneration process.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.

    Args:
        storyboard_id (UUID):
        body (CollectStoryboardGenerationParams):  Example: {'archetype_restriction':
            {'archetype_description': 'This format revolves around telling a personal or historical
            story in a compelling, narrative style. It focuses on building emotional connections
            through plot, characters, and personal experiences. Viewers are drawn in by the
            storytelling quality, relating to the journey or learning from past events.',
            'archetype_examples': ['How I Overcame My Fear of Public Speaking', 'The Untold Story
            Behind a 100-Year-Old Painting', 'My Experience Living in a Remote Village', 'Surviving a
            Near-Disaster: A Personal Account', 'A Grandmother’s Tale: Life Lessons from the 1950s'],
            'archetype_title': 'Storytelling Narrative'}, 'existing_content_summary': 'the pros and
            cons of different note-taking apps.', 'hard_restrictions': ['Duration < 5 minutes',
            'language = English', 'no profanity'], 'seed_keywords': ['handwriting to text goodnotes',
            'notability handwriting to text'], 'soft_restrictions': ['Use humor', 'feature dogs as
            characters']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StoryboardGenerationStatusDTO]
    """

    return sync_detailed(
        storyboard_id=storyboard_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CollectStoryboardGenerationParams,
) -> Response[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]:
    """Regenerate Storyboard

     Regenerate a storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard to regenerate.
    - **scenario_generation_inputs[CollectStoryboardGenerationParams]**: Input parameters for storyboard
    regeneration.

    Returns:
    - **StoryboardGenerationStatusDTO**: The status of the storyboard regeneration process.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.

    Args:
        storyboard_id (UUID):
        body (CollectStoryboardGenerationParams):  Example: {'archetype_restriction':
            {'archetype_description': 'This format revolves around telling a personal or historical
            story in a compelling, narrative style. It focuses on building emotional connections
            through plot, characters, and personal experiences. Viewers are drawn in by the
            storytelling quality, relating to the journey or learning from past events.',
            'archetype_examples': ['How I Overcame My Fear of Public Speaking', 'The Untold Story
            Behind a 100-Year-Old Painting', 'My Experience Living in a Remote Village', 'Surviving a
            Near-Disaster: A Personal Account', 'A Grandmother’s Tale: Life Lessons from the 1950s'],
            'archetype_title': 'Storytelling Narrative'}, 'existing_content_summary': 'the pros and
            cons of different note-taking apps.', 'hard_restrictions': ['Duration < 5 minutes',
            'language = English', 'no profanity'], 'seed_keywords': ['handwriting to text goodnotes',
            'notability handwriting to text'], 'soft_restrictions': ['Use humor', 'feature dogs as
            characters']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]
    """

    kwargs = _get_kwargs(
        storyboard_id=storyboard_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    storyboard_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CollectStoryboardGenerationParams,
) -> Optional[Union[HTTPValidationError, StoryboardGenerationStatusDTO]]:
    """Regenerate Storyboard

     Regenerate a storyboard by its ID.

    Args:
    - **storyboard_id**: The ID of the storyboard to regenerate.
    - **scenario_generation_inputs[CollectStoryboardGenerationParams]**: Input parameters for storyboard
    regeneration.

    Returns:
    - **StoryboardGenerationStatusDTO**: The status of the storyboard regeneration process.

    Raises:
    - **401 Unauthorized (PermissionException)**: Raised if the user is not authenticated.
    - **403 Forbidden (StoryboardAccessDenied)**: Raised if the storyboard does not exist or is
    inaccessible by the user.

    Args:
        storyboard_id (UUID):
        body (CollectStoryboardGenerationParams):  Example: {'archetype_restriction':
            {'archetype_description': 'This format revolves around telling a personal or historical
            story in a compelling, narrative style. It focuses on building emotional connections
            through plot, characters, and personal experiences. Viewers are drawn in by the
            storytelling quality, relating to the journey or learning from past events.',
            'archetype_examples': ['How I Overcame My Fear of Public Speaking', 'The Untold Story
            Behind a 100-Year-Old Painting', 'My Experience Living in a Remote Village', 'Surviving a
            Near-Disaster: A Personal Account', 'A Grandmother’s Tale: Life Lessons from the 1950s'],
            'archetype_title': 'Storytelling Narrative'}, 'existing_content_summary': 'the pros and
            cons of different note-taking apps.', 'hard_restrictions': ['Duration < 5 minutes',
            'language = English', 'no profanity'], 'seed_keywords': ['handwriting to text goodnotes',
            'notability handwriting to text'], 'soft_restrictions': ['Use humor', 'feature dogs as
            characters']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StoryboardGenerationStatusDTO]
    """

    return (
        await asyncio_detailed(
            storyboard_id=storyboard_id,
            client=client,
            body=body,
        )
    ).parsed
