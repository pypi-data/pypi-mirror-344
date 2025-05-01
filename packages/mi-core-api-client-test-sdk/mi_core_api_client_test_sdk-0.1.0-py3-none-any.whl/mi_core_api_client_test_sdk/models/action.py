from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.additional_workflow_actions import AdditionalWorkflowActions
from ..models.source_collect_type import SourceCollectType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Action")


@_attrs_define
class Action:
    """
    Attributes:
        type_ (Union[AdditionalWorkflowActions, SourceCollectType]):
        custom_fields_ids (Union[None, Unset, list[UUID]]):
        report_ids (Union[None, Unset, list[UUID]]):
    """

    type_: Union[AdditionalWorkflowActions, SourceCollectType]
    custom_fields_ids: Union[None, Unset, list[UUID]] = UNSET
    report_ids: Union[None, Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str
        if isinstance(self.type_, SourceCollectType):
            type_ = self.type_.value
        else:
            type_ = self.type_.value

        custom_fields_ids: Union[None, Unset, list[str]]
        if isinstance(self.custom_fields_ids, Unset):
            custom_fields_ids = UNSET
        elif isinstance(self.custom_fields_ids, list):
            custom_fields_ids = []
            for custom_fields_ids_type_0_item_data in self.custom_fields_ids:
                custom_fields_ids_type_0_item = str(custom_fields_ids_type_0_item_data)
                custom_fields_ids.append(custom_fields_ids_type_0_item)

        else:
            custom_fields_ids = self.custom_fields_ids

        report_ids: Union[None, Unset, list[str]]
        if isinstance(self.report_ids, Unset):
            report_ids = UNSET
        elif isinstance(self.report_ids, list):
            report_ids = []
            for report_ids_type_0_item_data in self.report_ids:
                report_ids_type_0_item = str(report_ids_type_0_item_data)
                report_ids.append(report_ids_type_0_item)

        else:
            report_ids = self.report_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if custom_fields_ids is not UNSET:
            field_dict["custom_fields_ids"] = custom_fields_ids
        if report_ids is not UNSET:
            field_dict["report_ids"] = report_ids

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

        def _parse_custom_fields_ids(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                custom_fields_ids_type_0 = []
                _custom_fields_ids_type_0 = data
                for custom_fields_ids_type_0_item_data in _custom_fields_ids_type_0:
                    custom_fields_ids_type_0_item = UUID(custom_fields_ids_type_0_item_data)

                    custom_fields_ids_type_0.append(custom_fields_ids_type_0_item)

                return custom_fields_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        custom_fields_ids = _parse_custom_fields_ids(d.pop("custom_fields_ids", UNSET))

        def _parse_report_ids(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                report_ids_type_0 = []
                _report_ids_type_0 = data
                for report_ids_type_0_item_data in _report_ids_type_0:
                    report_ids_type_0_item = UUID(report_ids_type_0_item_data)

                    report_ids_type_0.append(report_ids_type_0_item)

                return report_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        report_ids = _parse_report_ids(d.pop("report_ids", UNSET))

        action = cls(
            type_=type_,
            custom_fields_ids=custom_fields_ids,
            report_ids=report_ids,
        )

        action.additional_properties = d
        return action

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
