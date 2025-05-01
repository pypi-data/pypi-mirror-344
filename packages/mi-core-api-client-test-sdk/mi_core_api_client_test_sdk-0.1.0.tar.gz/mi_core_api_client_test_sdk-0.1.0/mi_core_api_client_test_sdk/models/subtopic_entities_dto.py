from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.over_time import OverTime


T = TypeVar("T", bound="SubtopicEntitiesDTO")


@_attrs_define
class SubtopicEntitiesDTO:
    """
    Attributes:
        name (str):
        quantity (int):
        entities (list[str]):
        over_time (Union[None, Unset, list['OverTime']]):
    """

    name: str
    quantity: int
    entities: list[str]
    over_time: Union[None, Unset, list["OverTime"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        quantity = self.quantity

        entities = self.entities

        over_time: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.over_time, Unset):
            over_time = UNSET
        elif isinstance(self.over_time, list):
            over_time = []
            for over_time_type_0_item_data in self.over_time:
                over_time_type_0_item = over_time_type_0_item_data.to_dict()
                over_time.append(over_time_type_0_item)

        else:
            over_time = self.over_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "quantity": quantity,
                "entities": entities,
            }
        )
        if over_time is not UNSET:
            field_dict["overTime"] = over_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.over_time import OverTime

        d = dict(src_dict)
        name = d.pop("name")

        quantity = d.pop("quantity")

        entities = cast(list[str], d.pop("entities"))

        def _parse_over_time(data: object) -> Union[None, Unset, list["OverTime"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                over_time_type_0 = []
                _over_time_type_0 = data
                for over_time_type_0_item_data in _over_time_type_0:
                    over_time_type_0_item = OverTime.from_dict(over_time_type_0_item_data)

                    over_time_type_0.append(over_time_type_0_item)

                return over_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["OverTime"]], data)

        over_time = _parse_over_time(d.pop("overTime", UNSET))

        subtopic_entities_dto = cls(
            name=name,
            quantity=quantity,
            entities=entities,
            over_time=over_time,
        )

        subtopic_entities_dto.additional_properties = d
        return subtopic_entities_dto

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
