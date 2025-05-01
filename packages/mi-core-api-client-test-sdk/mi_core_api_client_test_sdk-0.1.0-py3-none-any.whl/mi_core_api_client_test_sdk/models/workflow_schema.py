from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.action import Action


T = TypeVar("T", bound="WorkflowSchema")


@_attrs_define
class WorkflowSchema:
    """
    Attributes:
        name (str):
        cron_schedule (str):
        project_id (UUID):
        actions (list['Action']):
    """

    name: str
    cron_schedule: str
    project_id: UUID
    actions: list["Action"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        cron_schedule = self.cron_schedule

        project_id = str(self.project_id)

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "cron_schedule": cron_schedule,
                "project_id": project_id,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action import Action

        d = dict(src_dict)
        name = d.pop("name")

        cron_schedule = d.pop("cron_schedule")

        project_id = UUID(d.pop("project_id"))

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = Action.from_dict(actions_item_data)

            actions.append(actions_item)

        workflow_schema = cls(
            name=name,
            cron_schedule=cron_schedule,
            project_id=project_id,
            actions=actions,
        )

        workflow_schema.additional_properties = d
        return workflow_schema

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
