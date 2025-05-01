from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelArchitecture")


@_attrs_define
class ModelArchitecture:
    """
    Attributes:
        input_modalities (list[str]):
        output_modalities (list[str]):
        tokenizer (str):
        instruct_type (Union[None, Unset, str]):
    """

    input_modalities: list[str]
    output_modalities: list[str]
    tokenizer: str
    instruct_type: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_modalities = self.input_modalities

        output_modalities = self.output_modalities

        tokenizer = self.tokenizer

        instruct_type: Union[None, Unset, str]
        if isinstance(self.instruct_type, Unset):
            instruct_type = UNSET
        else:
            instruct_type = self.instruct_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputModalities": input_modalities,
                "outputModalities": output_modalities,
                "tokenizer": tokenizer,
            }
        )
        if instruct_type is not UNSET:
            field_dict["instructType"] = instruct_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_modalities = cast(list[str], d.pop("inputModalities"))

        output_modalities = cast(list[str], d.pop("outputModalities"))

        tokenizer = d.pop("tokenizer")

        def _parse_instruct_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instruct_type = _parse_instruct_type(d.pop("instructType", UNSET))

        model_architecture = cls(
            input_modalities=input_modalities,
            output_modalities=output_modalities,
            tokenizer=tokenizer,
            instruct_type=instruct_type,
        )

        model_architecture.additional_properties = d
        return model_architecture

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
