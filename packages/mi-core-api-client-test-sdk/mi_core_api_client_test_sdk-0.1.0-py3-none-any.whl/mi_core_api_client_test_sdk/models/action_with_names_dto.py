from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.additional_workflow_actions import AdditionalWorkflowActions
from ..models.source_collect_type import SourceCollectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ActionWithNamesDTO")


@_attrs_define
class ActionWithNamesDTO:
    """
    Attributes:
        type_ (Union[AdditionalWorkflowActions, SourceCollectType]):
        custom_fields_names (Union[Unset, list[str]]):
        report_names (Union[Unset, list[str]]):
    """

    type_: Union[AdditionalWorkflowActions, SourceCollectType]
    custom_fields_names: Union[Unset, list[str]] = UNSET
    report_names: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str
        if isinstance(self.type_, SourceCollectType):
            type_ = self.type_.value
        else:
            type_ = self.type_.value

        custom_fields_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.custom_fields_names, Unset):
            custom_fields_names = self.custom_fields_names

        report_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.report_names, Unset):
            report_names = self.report_names

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if custom_fields_names is not UNSET:
            field_dict["custom_fields_names"] = custom_fields_names
        if report_names is not UNSET:
            field_dict["report_names"] = report_names

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_type_(data: object) -> Union[AdditionalWorkflowActions, SourceCollectType]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_type_0 = SourceCollectType(data)

                return type_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            type_type_1 = AdditionalWorkflowActions(data)

            return type_type_1

        type_ = _parse_type_(d.pop("type"))

        custom_fields_names = cast(list[str], d.pop("custom_fields_names", UNSET))

        report_names = cast(list[str], d.pop("report_names", UNSET))

        action_with_names_dto = cls(
            type_=type_,
            custom_fields_names=custom_fields_names,
            report_names=report_names,
        )

        action_with_names_dto.additional_properties = d
        return action_with_names_dto

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
