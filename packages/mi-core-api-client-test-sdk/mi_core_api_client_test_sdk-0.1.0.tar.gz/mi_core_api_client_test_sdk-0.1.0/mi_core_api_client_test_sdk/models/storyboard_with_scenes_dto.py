from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_source_enum import InputSourceEnum
from ..models.storyboard_generation_status_enum import StoryboardGenerationStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.archetype_restriction import ArchetypeRestriction
    from ..models.base_storyboard_scene_dto import BaseStoryboardSceneDTO


T = TypeVar("T", bound="StoryboardWithScenesDTO")


@_attrs_define
class StoryboardWithScenesDTO:
    """
    Example:
        {'archetype_restriction': {'archetype_description': 'This format revolves around telling a personal or
            historical story in a compelling, narrative style. It focuses on building emotional connections through plot,
            characters, and personal experiences. Viewers are drawn in by the storytelling quality, relating to the journey
            or learning from past events.', 'archetype_examples': ['How I Overcame My Fear of Public Speaking', 'The Untold
            Story Behind a 100-Year-Old Painting', 'My Experience Living in a Remote Village', 'Surviving a Near-Disaster: A
            Personal Account', 'A Grandmother’s Tale: Life Lessons from the 1950s'], 'archetype_title': 'Storytelling
            Narrative'}, 'existing_content_summary': 'the pros and cons of different note-taking apps.',
            'hard_restrictions': ['Duration < 5 minutes', 'language = English', 'no profanity'], 'seed_keywords':
            ['handwriting to text goodnotes', 'notability handwriting to text'], 'soft_restrictions': ['Use humor', 'feature
            dogs as characters']}

    Attributes:
        seed_keywords (list[str]):
        input_source (InputSourceEnum): Enumeration class representing input source types.
        hard_restrictions (Union[None, Unset, list[str]]):
        soft_restrictions (Union[None, Unset, list[str]]):
        existing_content_summary (Union[None, Unset, str]):
        archetype_restriction (Union['ArchetypeRestriction', None, Unset]):
        id (Union[Unset, UUID]):
        status (Union[Unset, StoryboardGenerationStatusEnum]): Enumeration class representing storyboard generation
            status.
        title (Union[None, Unset, str]):
        thumbnail_url (Union[None, Unset, str]):
        scenes (Union[Unset, list['BaseStoryboardSceneDTO']]):
    """

    seed_keywords: list[str]
    input_source: InputSourceEnum
    hard_restrictions: Union[None, Unset, list[str]] = UNSET
    soft_restrictions: Union[None, Unset, list[str]] = UNSET
    existing_content_summary: Union[None, Unset, str] = UNSET
    archetype_restriction: Union["ArchetypeRestriction", None, Unset] = UNSET
    id: Union[Unset, UUID] = UNSET
    status: Union[Unset, StoryboardGenerationStatusEnum] = UNSET
    title: Union[None, Unset, str] = UNSET
    thumbnail_url: Union[None, Unset, str] = UNSET
    scenes: Union[Unset, list["BaseStoryboardSceneDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.archetype_restriction import ArchetypeRestriction

        seed_keywords = self.seed_keywords

        input_source = self.input_source.value

        hard_restrictions: Union[None, Unset, list[str]]
        if isinstance(self.hard_restrictions, Unset):
            hard_restrictions = UNSET
        elif isinstance(self.hard_restrictions, list):
            hard_restrictions = self.hard_restrictions

        else:
            hard_restrictions = self.hard_restrictions

        soft_restrictions: Union[None, Unset, list[str]]
        if isinstance(self.soft_restrictions, Unset):
            soft_restrictions = UNSET
        elif isinstance(self.soft_restrictions, list):
            soft_restrictions = self.soft_restrictions

        else:
            soft_restrictions = self.soft_restrictions

        existing_content_summary: Union[None, Unset, str]
        if isinstance(self.existing_content_summary, Unset):
            existing_content_summary = UNSET
        else:
            existing_content_summary = self.existing_content_summary

        archetype_restriction: Union[None, Unset, dict[str, Any]]
        if isinstance(self.archetype_restriction, Unset):
            archetype_restriction = UNSET
        elif isinstance(self.archetype_restriction, ArchetypeRestriction):
            archetype_restriction = self.archetype_restriction.to_dict()
        else:
            archetype_restriction = self.archetype_restriction

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        thumbnail_url: Union[None, Unset, str]
        if isinstance(self.thumbnail_url, Unset):
            thumbnail_url = UNSET
        else:
            thumbnail_url = self.thumbnail_url

        scenes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.scenes, Unset):
            scenes = []
            for scenes_item_data in self.scenes:
                scenes_item = scenes_item_data.to_dict()
                scenes.append(scenes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seedKeywords": seed_keywords,
                "inputSource": input_source,
            }
        )
        if hard_restrictions is not UNSET:
            field_dict["hardRestrictions"] = hard_restrictions
        if soft_restrictions is not UNSET:
            field_dict["softRestrictions"] = soft_restrictions
        if existing_content_summary is not UNSET:
            field_dict["existingContentSummary"] = existing_content_summary
        if archetype_restriction is not UNSET:
            field_dict["archetypeRestriction"] = archetype_restriction
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if title is not UNSET:
            field_dict["title"] = title
        if thumbnail_url is not UNSET:
            field_dict["thumbnailUrl"] = thumbnail_url
        if scenes is not UNSET:
            field_dict["scenes"] = scenes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.archetype_restriction import ArchetypeRestriction
        from ..models.base_storyboard_scene_dto import BaseStoryboardSceneDTO

        d = dict(src_dict)
        seed_keywords = cast(list[str], d.pop("seedKeywords"))

        input_source = InputSourceEnum(d.pop("inputSource"))

        def _parse_hard_restrictions(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                hard_restrictions_type_0 = cast(list[str], data)

                return hard_restrictions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        hard_restrictions = _parse_hard_restrictions(d.pop("hardRestrictions", UNSET))

        def _parse_soft_restrictions(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                soft_restrictions_type_0 = cast(list[str], data)

                return soft_restrictions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        soft_restrictions = _parse_soft_restrictions(d.pop("softRestrictions", UNSET))

        def _parse_existing_content_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        existing_content_summary = _parse_existing_content_summary(d.pop("existingContentSummary", UNSET))

        def _parse_archetype_restriction(data: object) -> Union["ArchetypeRestriction", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                archetype_restriction_type_0 = ArchetypeRestriction.from_dict(data)

                return archetype_restriction_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ArchetypeRestriction", None, Unset], data)

        archetype_restriction = _parse_archetype_restriction(d.pop("archetypeRestriction", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _status = d.pop("status", UNSET)
        status: Union[Unset, StoryboardGenerationStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = StoryboardGenerationStatusEnum(_status)

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_thumbnail_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thumbnail_url = _parse_thumbnail_url(d.pop("thumbnailUrl", UNSET))

        scenes = []
        _scenes = d.pop("scenes", UNSET)
        for scenes_item_data in _scenes or []:
            scenes_item = BaseStoryboardSceneDTO.from_dict(scenes_item_data)

            scenes.append(scenes_item)

        storyboard_with_scenes_dto = cls(
            seed_keywords=seed_keywords,
            input_source=input_source,
            hard_restrictions=hard_restrictions,
            soft_restrictions=soft_restrictions,
            existing_content_summary=existing_content_summary,
            archetype_restriction=archetype_restriction,
            id=id,
            status=status,
            title=title,
            thumbnail_url=thumbnail_url,
            scenes=scenes,
        )

        storyboard_with_scenes_dto.additional_properties = d
        return storyboard_with_scenes_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
