from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coverage import Coverage
    from ..models.subtopic_entities_dto import SubtopicEntitiesDTO


T = TypeVar("T", bound="GraphExtractionDTO")


@_attrs_define
class GraphExtractionDTO:
    """
    Attributes:
        topic (str):
        subtopics (list['SubtopicEntitiesDTO']):
        coverage (Union['Coverage', None, Unset]):
    """

    topic: str
    subtopics: list["SubtopicEntitiesDTO"]
    coverage: Union["Coverage", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.coverage import Coverage

        topic = self.topic

        subtopics = []
        for subtopics_item_data in self.subtopics:
            subtopics_item = subtopics_item_data.to_dict()
            subtopics.append(subtopics_item)

        coverage: Union[None, Unset, dict[str, Any]]
        if isinstance(self.coverage, Unset):
            coverage = UNSET
        elif isinstance(self.coverage, Coverage):
            coverage = self.coverage.to_dict()
        else:
            coverage = self.coverage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic": topic,
                "subtopics": subtopics,
            }
        )
        if coverage is not UNSET:
            field_dict["coverage"] = coverage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.coverage import Coverage
        from ..models.subtopic_entities_dto import SubtopicEntitiesDTO

        d = dict(src_dict)
        topic = d.pop("topic")

        subtopics = []
        _subtopics = d.pop("subtopics")
        for subtopics_item_data in _subtopics:
            subtopics_item = SubtopicEntitiesDTO.from_dict(subtopics_item_data)

            subtopics.append(subtopics_item)

        def _parse_coverage(data: object) -> Union["Coverage", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                coverage_type_0 = Coverage.from_dict(data)

                return coverage_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Coverage", None, Unset], data)

        coverage = _parse_coverage(d.pop("coverage", UNSET))

        graph_extraction_dto = cls(
            topic=topic,
            subtopics=subtopics,
            coverage=coverage,
        )

        graph_extraction_dto.additional_properties = d
        return graph_extraction_dto

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
