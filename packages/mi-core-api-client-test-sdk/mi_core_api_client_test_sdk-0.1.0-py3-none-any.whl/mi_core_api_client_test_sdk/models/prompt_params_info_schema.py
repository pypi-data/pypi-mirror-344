from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.prompt_params_info_schema_outputparams import PromptParamsInfoSchemaOutputparams


T = TypeVar("T", bound="PromptParamsInfoSchema")


@_attrs_define
class PromptParamsInfoSchema:
    """
    Attributes:
        input_params (list[str]):
        output_params (PromptParamsInfoSchemaOutputparams):
    """

    input_params: list[str]
    output_params: "PromptParamsInfoSchemaOutputparams"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_params = self.input_params

        output_params = self.output_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inputParams": input_params,
                "outputParams": output_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prompt_params_info_schema_outputparams import PromptParamsInfoSchemaOutputparams

        d = dict(src_dict)
        input_params = cast(list[str], d.pop("inputParams"))

        output_params = PromptParamsInfoSchemaOutputparams.from_dict(d.pop("outputParams"))

        prompt_params_info_schema = cls(
            input_params=input_params,
            output_params=output_params,
        )

        prompt_params_info_schema.additional_properties = d
        return prompt_params_info_schema

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
