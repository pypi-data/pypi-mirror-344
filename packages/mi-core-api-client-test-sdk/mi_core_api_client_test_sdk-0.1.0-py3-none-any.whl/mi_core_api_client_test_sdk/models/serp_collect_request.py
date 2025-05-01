from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SerpCollectRequest")


@_attrs_define
class SerpCollectRequest:
    """
    Example:
        {'related_topics': ['GSC Game World', 'Chernobyl Exclusion Zone', 'survival horror', 'open-world gameplay', 'PC
            gaming']}

    Attributes:
        related_topics (list[str]):
    """

    related_topics: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        related_topics = self.related_topics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "related_topics": related_topics,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        related_topics = cast(list[str], d.pop("related_topics"))

        serp_collect_request = cls(
            related_topics=related_topics,
        )

        serp_collect_request.additional_properties = d
        return serp_collect_request

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
