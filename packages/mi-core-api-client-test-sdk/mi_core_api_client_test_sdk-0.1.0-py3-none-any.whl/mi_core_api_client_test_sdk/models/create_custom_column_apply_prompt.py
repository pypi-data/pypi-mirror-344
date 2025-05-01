from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_field_type import CustomFieldType

T = TypeVar("T", bound="CreateCustomColumnApplyPrompt")


@_attrs_define
class CreateCustomColumnApplyPrompt:
    """
    Attributes:
        content_type (CustomFieldType): Enumeration class representing custom field types.
        model (str):
        prompt (str):
        name (str):
        type_ (Literal['apply_prompt']):
        project_id (UUID):
    """

    content_type: CustomFieldType
    model: str
    prompt: str
    name: str
    type_: Literal["apply_prompt"]
    project_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type.value

        model = self.model

        prompt = self.prompt

        name = self.name

        type_ = self.type_

        project_id = str(self.project_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_type": content_type,
                "model": model,
                "prompt": prompt,
                "name": name,
                "type": type_,
                "project_id": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = CustomFieldType(d.pop("content_type"))

        model = d.pop("model")

        prompt = d.pop("prompt")

        name = d.pop("name")

        type_ = cast(Literal["apply_prompt"], d.pop("type"))
        if type_ != "apply_prompt":
            raise ValueError(f"type must match const 'apply_prompt', got '{type_}'")

        project_id = UUID(d.pop("project_id"))

        create_custom_column_apply_prompt = cls(
            content_type=content_type,
            model=model,
            prompt=prompt,
            name=name,
            type_=type_,
            project_id=project_id,
        )

        create_custom_column_apply_prompt.additional_properties = d
        return create_custom_column_apply_prompt

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
