from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_job_execution_metadata import RunJobExecutionMetadata
    from ..models.workflow_action_execution_metadata import WorkflowActionExecutionMetadata


T = TypeVar("T", bound="WorkflowExecutionMetadata")


@_attrs_define
class WorkflowExecutionMetadata:
    """
    Attributes:
        job_execution (RunJobExecutionMetadata):
        actions (Union[Unset, list['WorkflowActionExecutionMetadata']]):
    """

    job_execution: "RunJobExecutionMetadata"
    actions: Union[Unset, list["WorkflowActionExecutionMetadata"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_execution = self.job_execution.to_dict()

        actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_execution": job_execution,
            }
        )
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_job_execution_metadata import RunJobExecutionMetadata
        from ..models.workflow_action_execution_metadata import WorkflowActionExecutionMetadata

        d = dict(src_dict)
        job_execution = RunJobExecutionMetadata.from_dict(d.pop("job_execution"))

        actions = []
        _actions = d.pop("actions", UNSET)
        for actions_item_data in _actions or []:
            actions_item = WorkflowActionExecutionMetadata.from_dict(actions_item_data)

            actions.append(actions_item)

        workflow_execution_metadata = cls(
            job_execution=job_execution,
            actions=actions,
        )

        workflow_execution_metadata.additional_properties = d
        return workflow_execution_metadata

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
