from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_type import CustomFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateCustomColumnApplyPrompt")


@_attrs_define
class UpdateCustomColumnApplyPrompt:
    """
    Attributes:
        content_type (CustomFieldType): Enumeration class representing custom field types.
        type_ (Literal['apply_prompt']):
        model (Union[None, Unset, str]):
        prompt (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
    """

    content_type: CustomFieldType
    type_: Literal["apply_prompt"]
    model: Union[None, Unset, str] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type.value

        type_ = self.type_

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_type": content_type,
                "type": type_,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = CustomFieldType(d.pop("content_type"))

        type_ = cast(Literal["apply_prompt"], d.pop("type"))
        if type_ != "apply_prompt":
            raise ValueError(f"type must match const 'apply_prompt', got '{type_}'")

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        update_custom_column_apply_prompt = cls(
            content_type=content_type,
            type_=type_,
            model=model,
            prompt=prompt,
            name=name,
        )

        update_custom_column_apply_prompt.additional_properties = d
        return update_custom_column_apply_prompt

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
