from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ArchetypeRestriction")


@_attrs_define
class ArchetypeRestriction:
    """
    Attributes:
        archetype_title (str):
        archetype_description (str):
        archetype_examples (list[str]):
    """

    archetype_title: str
    archetype_description: str
    archetype_examples: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        archetype_title = self.archetype_title

        archetype_description = self.archetype_description

        archetype_examples = self.archetype_examples

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "archetypeTitle": archetype_title,
                "archetypeDescription": archetype_description,
                "archetypeExamples": archetype_examples,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        archetype_title = d.pop("archetypeTitle")

        archetype_description = d.pop("archetypeDescription")

        archetype_examples = cast(list[str], d.pop("archetypeExamples"))

        archetype_restriction = cls(
            archetype_title=archetype_title,
            archetype_description=archetype_description,
            archetype_examples=archetype_examples,
        )

        archetype_restriction.additional_properties = d
        return archetype_restriction

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
