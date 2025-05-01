from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action import Action


T = TypeVar("T", bound="WorkflowUpdateSchema")


@_attrs_define
class WorkflowUpdateSchema:
    """
    Attributes:
        project_id (UUID):
        name (Union[None, Unset, str]):
        cron_schedule (Union[None, Unset, str]):
        actions (Union[None, Unset, list['Action']]):
    """

    project_id: UUID
    name: Union[None, Unset, str] = UNSET
    cron_schedule: Union[None, Unset, str] = UNSET
    actions: Union[None, Unset, list["Action"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = str(self.project_id)

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        cron_schedule: Union[None, Unset, str]
        if isinstance(self.cron_schedule, Unset):
            cron_schedule = UNSET
        else:
            cron_schedule = self.cron_schedule

        actions: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.actions, Unset):
            actions = UNSET
        elif isinstance(self.actions, list):
            actions = []
            for actions_type_0_item_data in self.actions:
                actions_type_0_item = actions_type_0_item_data.to_dict()
                actions.append(actions_type_0_item)

        else:
            actions = self.actions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_id": project_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if cron_schedule is not UNSET:
            field_dict["cron_schedule"] = cron_schedule
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action import Action

        d = dict(src_dict)
        project_id = UUID(d.pop("project_id"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_cron_schedule(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cron_schedule = _parse_cron_schedule(d.pop("cron_schedule", UNSET))

        def _parse_actions(data: object) -> Union[None, Unset, list["Action"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                actions_type_0 = []
                _actions_type_0 = data
                for actions_type_0_item_data in _actions_type_0:
                    actions_type_0_item = Action.from_dict(actions_type_0_item_data)

                    actions_type_0.append(actions_type_0_item)

                return actions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["Action"]], data)

        actions = _parse_actions(d.pop("actions", UNSET))

        workflow_update_schema = cls(
            project_id=project_id,
            name=name,
            cron_schedule=cron_schedule,
            actions=actions,
        )

        workflow_update_schema.additional_properties = d
        return workflow_update_schema

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
