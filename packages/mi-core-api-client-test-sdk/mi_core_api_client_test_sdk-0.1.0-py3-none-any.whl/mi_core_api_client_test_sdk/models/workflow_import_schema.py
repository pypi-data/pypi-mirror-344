from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action_dto import ActionDTO
    from ..models.action_with_names_dto import ActionWithNamesDTO


T = TypeVar("T", bound="WorkflowImportSchema")


@_attrs_define
class WorkflowImportSchema:
    """
    Attributes:
        name (str):
        cron_schedule (str):
        actions (list[Union['ActionDTO', 'ActionWithNamesDTO']]):
        user_id (UUID):
        is_active (Union[Unset, bool]):  Default: True.
    """

    name: str
    cron_schedule: str
    actions: list[Union["ActionDTO", "ActionWithNamesDTO"]]
    user_id: UUID
    is_active: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.action_with_names_dto import ActionWithNamesDTO

        name = self.name

        cron_schedule = self.cron_schedule

        actions = []
        for actions_item_data in self.actions:
            actions_item: dict[str, Any]
            if isinstance(actions_item_data, ActionWithNamesDTO):
                actions_item = actions_item_data.to_dict()
            else:
                actions_item = actions_item_data.to_dict()

            actions.append(actions_item)

        user_id = str(self.user_id)

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "cronSchedule": cron_schedule,
                "actions": actions,
                "userId": user_id,
            }
        )
        if is_active is not UNSET:
            field_dict["isActive"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action_dto import ActionDTO
        from ..models.action_with_names_dto import ActionWithNamesDTO

        d = dict(src_dict)
        name = d.pop("name")

        cron_schedule = d.pop("cronSchedule")

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:

            def _parse_actions_item(data: object) -> Union["ActionDTO", "ActionWithNamesDTO"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_0 = ActionWithNamesDTO.from_dict(data)

                    return actions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                actions_item_type_1 = ActionDTO.from_dict(data)

                return actions_item_type_1

            actions_item = _parse_actions_item(actions_item_data)

            actions.append(actions_item)

        user_id = UUID(d.pop("userId"))

        is_active = d.pop("isActive", UNSET)

        workflow_import_schema = cls(
            name=name,
            cron_schedule=cron_schedule,
            actions=actions,
            user_id=user_id,
            is_active=is_active,
        )

        workflow_import_schema.additional_properties = d
        return workflow_import_schema

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
