from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.source_types import SourceTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContentItemSource")


@_attrs_define
class ContentItemSource:
    """
    Attributes:
        type_ (SourceTypes): Enumeration class representing source types.
        input_query (Union[None, Unset, str]):
        input_url (Union[None, Unset, str]):
    """

    type_: SourceTypes
    input_query: Union[None, Unset, str] = UNSET
    input_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        input_query: Union[None, Unset, str]
        if isinstance(self.input_query, Unset):
            input_query = UNSET
        else:
            input_query = self.input_query

        input_url: Union[None, Unset, str]
        if isinstance(self.input_url, Unset):
            input_url = UNSET
        else:
            input_url = self.input_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if input_query is not UNSET:
            field_dict["inputQuery"] = input_query
        if input_url is not UNSET:
            field_dict["inputUrl"] = input_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = SourceTypes(d.pop("type"))

        def _parse_input_query(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_query = _parse_input_query(d.pop("inputQuery", UNSET))

        def _parse_input_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_url = _parse_input_url(d.pop("inputUrl", UNSET))

        content_item_source = cls(
            type_=type_,
            input_query=input_query,
            input_url=input_url,
        )

        content_item_source.additional_properties = d
        return content_item_source

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
