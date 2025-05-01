from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.prompt_type import PromptType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptUpdateSchema")


@_attrs_define
class PromptUpdateSchema:
    """
    Attributes:
        title (Union[None, Unset, str]):
        prompt_type (Union[None, PromptType, Unset]):
        prompt_text (Union[None, Unset, str]):
    """

    title: Union[None, Unset, str] = UNSET
    prompt_type: Union[None, PromptType, Unset] = UNSET
    prompt_text: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        prompt_type: Union[None, Unset, str]
        if isinstance(self.prompt_type, Unset):
            prompt_type = UNSET
        elif isinstance(self.prompt_type, PromptType):
            prompt_type = self.prompt_type.value
        else:
            prompt_type = self.prompt_type

        prompt_text: Union[None, Unset, str]
        if isinstance(self.prompt_text, Unset):
            prompt_text = UNSET
        else:
            prompt_text = self.prompt_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if prompt_type is not UNSET:
            field_dict["prompt_type"] = prompt_type
        if prompt_text is not UNSET:
            field_dict["prompt_text"] = prompt_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_prompt_type(data: object) -> Union[None, PromptType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                prompt_type_type_0 = PromptType(data)

                return prompt_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, PromptType, Unset], data)

        prompt_type = _parse_prompt_type(d.pop("prompt_type", UNSET))

        def _parse_prompt_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt_text = _parse_prompt_text(d.pop("prompt_text", UNSET))

        prompt_update_schema = cls(
            title=title,
            prompt_type=prompt_type,
            prompt_text=prompt_text,
        )

        prompt_update_schema.additional_properties = d
        return prompt_update_schema

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
