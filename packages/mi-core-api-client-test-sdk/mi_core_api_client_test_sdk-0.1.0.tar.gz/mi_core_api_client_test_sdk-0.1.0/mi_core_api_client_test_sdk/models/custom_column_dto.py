from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_column_type import CustomColumnType
from ..models.custom_field_type import CustomFieldType
from ..models.data_lookup_model import DataLookupModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomColumnDTO")


@_attrs_define
class CustomColumnDTO:
    """
    Attributes:
        type_ (CustomColumnType): Enumeration class representing custom column types.
        content_type (CustomFieldType): Enumeration class representing custom field types.
        name (str):
        project_id (UUID):
        valid_answers (Union[None, Unset, list[str]]):
        prompt (Union[None, Unset, str]):
        model (Union[None, Unset, str]):
        auto (Union[Unset, bool]):  Default: False.
        lookup_model (Union[DataLookupModel, None, Unset]):
        lookup_field (Union[None, Unset, str]):
        id (Union[Unset, UUID]):
    """

    type_: CustomColumnType
    content_type: CustomFieldType
    name: str
    project_id: UUID
    valid_answers: Union[None, Unset, list[str]] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    model: Union[None, Unset, str] = UNSET
    auto: Union[Unset, bool] = False
    lookup_model: Union[DataLookupModel, None, Unset] = UNSET
    lookup_field: Union[None, Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        content_type = self.content_type.value

        name = self.name

        project_id = str(self.project_id)

        valid_answers: Union[None, Unset, list[str]]
        if isinstance(self.valid_answers, Unset):
            valid_answers = UNSET
        elif isinstance(self.valid_answers, list):
            valid_answers = self.valid_answers

        else:
            valid_answers = self.valid_answers

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        auto = self.auto

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

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "contentType": content_type,
                "name": name,
                "projectId": project_id,
            }
        )
        if valid_answers is not UNSET:
            field_dict["validAnswers"] = valid_answers
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if model is not UNSET:
            field_dict["model"] = model
        if auto is not UNSET:
            field_dict["auto"] = auto
        if lookup_model is not UNSET:
            field_dict["lookupModel"] = lookup_model
        if lookup_field is not UNSET:
            field_dict["lookupField"] = lookup_field
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = CustomColumnType(d.pop("type"))

        content_type = CustomFieldType(d.pop("contentType"))

        name = d.pop("name")

        project_id = UUID(d.pop("projectId"))

        def _parse_valid_answers(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                valid_answers_type_0 = cast(list[str], data)

                return valid_answers_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        valid_answers = _parse_valid_answers(d.pop("validAnswers", UNSET))

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        auto = d.pop("auto", UNSET)

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

        lookup_model = _parse_lookup_model(d.pop("lookupModel", UNSET))

        def _parse_lookup_field(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        lookup_field = _parse_lookup_field(d.pop("lookupField", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        custom_column_dto = cls(
            type_=type_,
            content_type=content_type,
            name=name,
            project_id=project_id,
            valid_answers=valid_answers,
            prompt=prompt,
            model=model,
            auto=auto,
            lookup_model=lookup_model,
            lookup_field=lookup_field,
            id=id,
        )

        custom_column_dto.additional_properties = d
        return custom_column_dto

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
