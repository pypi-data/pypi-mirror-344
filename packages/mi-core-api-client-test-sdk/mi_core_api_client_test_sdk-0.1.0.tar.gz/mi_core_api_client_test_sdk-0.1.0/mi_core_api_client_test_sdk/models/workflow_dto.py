import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action_dto import ActionDTO


T = TypeVar("T", bound="WorkflowDTO")


@_attrs_define
class WorkflowDTO:
    """
    Attributes:
        name (str):
        cron_schedule (str):
        project_id (UUID):
        actions (list['ActionDTO']):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        id (Union[Unset, UUID]):
        is_active (Union[Unset, bool]):  Default: True.
    """

    name: str
    cron_schedule: str
    project_id: UUID
    actions: list["ActionDTO"]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: Union[Unset, UUID] = UNSET
    is_active: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        cron_schedule = self.cron_schedule

        project_id = str(self.project_id)

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "cronSchedule": cron_schedule,
                "projectId": project_id,
                "actions": actions,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if is_active is not UNSET:
            field_dict["isActive"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action_dto import ActionDTO

        d = dict(src_dict)
        name = d.pop("name")

        cron_schedule = d.pop("cronSchedule")

        project_id = UUID(d.pop("projectId"))

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = ActionDTO.from_dict(actions_item_data)

            actions.append(actions_item)

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        is_active = d.pop("isActive", UNSET)

        workflow_dto = cls(
            name=name,
            cron_schedule=cron_schedule,
            project_id=project_id,
            actions=actions,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
            is_active=is_active,
        )

        workflow_dto.additional_properties = d
        return workflow_dto

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
