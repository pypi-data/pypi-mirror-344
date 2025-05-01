from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_type import CustomFieldType
from ..models.data_lookup_model import DataLookupModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateCustomColumnDataLookup")


@_attrs_define
class UpdateCustomColumnDataLookup:
    """
    Attributes:
        type_ (Literal['data_lookup']):
        content_type (CustomFieldType): Enumeration class representing custom field types.
        name (Union[None, Unset, str]):
        lookup_model (Union[DataLookupModel, None, Unset]):
        lookup_field (Union[None, Unset, str]):
    """

    type_: Literal["data_lookup"]
    content_type: CustomFieldType
    name: Union[None, Unset, str] = UNSET
    lookup_model: Union[DataLookupModel, None, Unset] = UNSET
    lookup_field: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        content_type = self.content_type.value

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        lookup_model: Union[None, Unset, str]
        if isinstance(self.lookup_model, Unset):
            lookup_model = UNSET
        elif isinstance(self.lookup_model, DataLookupModel):
            lookup_model = self.lookup_model.value
        else:
            lookup_model = self.lookup_model

        lookup_field: Union[None, Unset, str]
        if isinstance(self.lookup_field, Unset):
            lookup_field = UNSET
        else:
            lookup_field = self.lookup_field

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "content_type": content_type,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if lookup_model is not UNSET:
            field_dict["lookup_model"] = lookup_model
        if lookup_field is not UNSET:
            field_dict["lookup_field"] = lookup_field

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["data_lookup"], d.pop("type"))
        if type_ != "data_lookup":
            raise ValueError(f"type must match const 'data_lookup', got '{type_}'")

        content_type = CustomFieldType(d.pop("content_type"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_lookup_model(data: object) -> Union[DataLookupModel, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                lookup_model_type_0 = DataLookupModel(data)

                return lookup_model_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DataLookupModel, None, Unset], data)

        lookup_model = _parse_lookup_model(d.pop("lookup_model", UNSET))

        def _parse_lookup_field(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        lookup_field = _parse_lookup_field(d.pop("lookup_field", UNSET))

        update_custom_column_data_lookup = cls(
            type_=type_,
            content_type=content_type,
            name=name,
            lookup_model=lookup_model,
            lookup_field=lookup_field,
        )

        update_custom_column_data_lookup.additional_properties = d
        return update_custom_column_data_lookup

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
