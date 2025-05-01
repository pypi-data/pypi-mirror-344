from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.archetype_restriction import ArchetypeRestriction


T = TypeVar("T", bound="CollectStoryboardGenerationParams")


@_attrs_define
class CollectStoryboardGenerationParams:
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
        hard_restrictions (Union[None, Unset, list[str]]):
        soft_restrictions (Union[None, Unset, list[str]]):
        existing_content_summary (Union[None, Unset, str]):
        archetype_restriction (Union['ArchetypeRestriction', None, Unset]):
    """

    seed_keywords: list[str]
    hard_restrictions: Union[None, Unset, list[str]] = UNSET
    soft_restrictions: Union[None, Unset, list[str]] = UNSET
    existing_content_summary: Union[None, Unset, str] = UNSET
    archetype_restriction: Union["ArchetypeRestriction", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.archetype_restriction import ArchetypeRestriction

        seed_keywords = self.seed_keywords

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "seedKeywords": seed_keywords,
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.archetype_restriction import ArchetypeRestriction

        d = dict(src_dict)
        seed_keywords = cast(list[str], d.pop("seedKeywords"))

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

        collect_storyboard_generation_params = cls(
            seed_keywords=seed_keywords,
            hard_restrictions=hard_restrictions,
            soft_restrictions=soft_restrictions,
            existing_content_summary=existing_content_summary,
            archetype_restriction=archetype_restriction,
        )

        collect_storyboard_generation_params.additional_properties = d
        return collect_storyboard_generation_params

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
