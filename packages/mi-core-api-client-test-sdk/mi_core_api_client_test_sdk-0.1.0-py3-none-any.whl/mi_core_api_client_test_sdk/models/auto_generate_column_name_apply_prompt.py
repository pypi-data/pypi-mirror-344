from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_type import CustomFieldType

T = TypeVar("T", bound="AutoGenerateColumnNameApplyPrompt")


@_attrs_define
class AutoGenerateColumnNameApplyPrompt:
    """
    Attributes:
        content_type (CustomFieldType): Enumeration class representing custom field types.
        model (str):
        prompt (str):
        type_ (Literal['apply_prompt']):
    """

    content_type: CustomFieldType
    model: str
    prompt: str
    type_: Literal["apply_prompt"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type.value

        model = self.model

        prompt = self.prompt

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_type": content_type,
                "model": model,
                "prompt": prompt,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = CustomFieldType(d.pop("content_type"))

        model = d.pop("model")

        prompt = d.pop("prompt")

        type_ = cast(Literal["apply_prompt"], d.pop("type"))
        if type_ != "apply_prompt":
            raise ValueError(f"type must match const 'apply_prompt', got '{type_}'")

        auto_generate_column_name_apply_prompt = cls(
            content_type=content_type,
            model=model,
            prompt=prompt,
            type_=type_,
        )

        auto_generate_column_name_apply_prompt.additional_properties = d
        return auto_generate_column_name_apply_prompt

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
