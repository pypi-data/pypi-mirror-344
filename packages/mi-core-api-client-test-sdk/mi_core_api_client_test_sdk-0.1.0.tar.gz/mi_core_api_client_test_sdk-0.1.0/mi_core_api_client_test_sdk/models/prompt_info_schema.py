from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.prompt_type import PromptType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PromptInfoSchema")


@_attrs_define
class PromptInfoSchema:
    """
    Attributes:
        prompt_type (PromptType): Enumeration class representing prompt types.
        prompt_text (str):
        id (UUID):
        is_active (bool):
        title (Union[None, Unset, str]):
    """

    prompt_type: PromptType
    prompt_text: str
    id: UUID
    is_active: bool
    title: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt_type = self.prompt_type.value

        prompt_text = self.prompt_text

        id = str(self.id)

        is_active = self.is_active

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "promptType": prompt_type,
                "promptText": prompt_text,
                "id": id,
                "isActive": is_active,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prompt_type = PromptType(d.pop("promptType"))

        prompt_text = d.pop("promptText")

        id = UUID(d.pop("id"))

        is_active = d.pop("isActive")

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        prompt_info_schema = cls(
            prompt_type=prompt_type,
            prompt_text=prompt_text,
            id=id,
            is_active=is_active,
            title=title,
        )

        prompt_info_schema.additional_properties = d
        return prompt_info_schema

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
