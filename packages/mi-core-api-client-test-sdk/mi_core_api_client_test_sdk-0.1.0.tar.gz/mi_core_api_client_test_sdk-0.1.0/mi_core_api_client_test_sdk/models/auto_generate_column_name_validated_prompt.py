from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_type import CustomFieldType

T = TypeVar("T", bound="AutoGenerateColumnNameValidatedPrompt")


@_attrs_define
class AutoGenerateColumnNameValidatedPrompt:
    """
    Attributes:
        content_type (CustomFieldType): Enumeration class representing custom field types.
        model (str):
        prompt (str):
        type_ (Literal['validated_prompt']):
        valid_answers (list[str]):
    """

    content_type: CustomFieldType
    model: str
    prompt: str
    type_: Literal["validated_prompt"]
    valid_answers: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type.value

        model = self.model

        prompt = self.prompt

        type_ = self.type_

        valid_answers = self.valid_answers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_type": content_type,
                "model": model,
                "prompt": prompt,
                "type": type_,
                "valid_answers": valid_answers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = CustomFieldType(d.pop("content_type"))

        model = d.pop("model")

        prompt = d.pop("prompt")

        type_ = cast(Literal["validated_prompt"], d.pop("type"))
        if type_ != "validated_prompt":
            raise ValueError(f"type must match const 'validated_prompt', got '{type_}'")

        valid_answers = cast(list[str], d.pop("valid_answers"))

        auto_generate_column_name_validated_prompt = cls(
            content_type=content_type,
            model=model,
            prompt=prompt,
            type_=type_,
            valid_answers=valid_answers,
        )

        auto_generate_column_name_validated_prompt.additional_properties = d
        return auto_generate_column_name_validated_prompt

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
