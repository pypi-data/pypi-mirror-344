from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.collect_serp_data_serpresults import CollectSerpDataSerpresults


T = TypeVar("T", bound="CollectSerpData")


@_attrs_define
class CollectSerpData:
    """
    Attributes:
        serp_results (CollectSerpDataSerpresults):
    """

    serp_results: "CollectSerpDataSerpresults"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        serp_results = self.serp_results.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serpResults": serp_results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.collect_serp_data_serpresults import CollectSerpDataSerpresults

        d = dict(src_dict)
        serp_results = CollectSerpDataSerpresults.from_dict(d.pop("serpResults"))

        collect_serp_data = cls(
            serp_results=serp_results,
        )

        collect_serp_data.additional_properties = d
        return collect_serp_data

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
