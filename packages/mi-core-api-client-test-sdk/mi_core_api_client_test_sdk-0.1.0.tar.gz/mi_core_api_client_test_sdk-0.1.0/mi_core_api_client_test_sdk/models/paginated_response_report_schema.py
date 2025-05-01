from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.report_schema import ReportSchema


T = TypeVar("T", bound="PaginatedResponseReportSchema")


@_attrs_define
class PaginatedResponseReportSchema:
    """
    Attributes:
        count (int): Number of total items
        total_pages (int): Number of total pages
        input_items (Union[Unset, list['ReportSchema']]): List of items before pagination
    """

    count: int
    total_pages: int
    input_items: Union[Unset, list["ReportSchema"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        total_pages = self.total_pages

        input_items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.input_items, Unset):
            input_items = []
            for input_items_item_data in self.input_items:
                input_items_item = input_items_item_data.to_dict()
                input_items.append(input_items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "totalPages": total_pages,
            }
        )
        if input_items is not UNSET:
            field_dict["inputItems"] = input_items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.report_schema import ReportSchema

        d = dict(src_dict)
        count = d.pop("count")

        total_pages = d.pop("totalPages")

        input_items = []
        _input_items = d.pop("inputItems", UNSET)
        for input_items_item_data in _input_items or []:
            input_items_item = ReportSchema.from_dict(input_items_item_data)

            input_items.append(input_items_item)

        paginated_response_report_schema = cls(
            count=count,
            total_pages=total_pages,
            input_items=input_items,
        )

        paginated_response_report_schema.additional_properties = d
        return paginated_response_report_schema

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
