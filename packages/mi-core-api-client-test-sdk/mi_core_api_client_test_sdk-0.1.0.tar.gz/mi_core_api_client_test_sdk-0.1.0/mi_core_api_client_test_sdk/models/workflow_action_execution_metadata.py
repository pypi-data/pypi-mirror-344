from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_status import ExecutionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action import Action
    from ..models.project_sources_collection_stats import ProjectSourcesCollectionStats


T = TypeVar("T", bound="WorkflowActionExecutionMetadata")


@_attrs_define
class WorkflowActionExecutionMetadata:
    """
    Attributes:
        action (Action):
        status (ExecutionStatus): Enumeration class representing workflow execution statuses.

            Attributes:
                INITIALIZED: Represents initialized job status.
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
                TERMINATED: Represents terminated job status.
        error_message (Union[None, Unset, str]):
        source_stats (Union['ProjectSourcesCollectionStats', None, Unset]):
    """

    action: "Action"
    status: ExecutionStatus
    error_message: Union[None, Unset, str] = UNSET
    source_stats: Union["ProjectSourcesCollectionStats", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_sources_collection_stats import ProjectSourcesCollectionStats

        action = self.action.to_dict()

        status = self.status.value

        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        source_stats: Union[None, Unset, dict[str, Any]]
        if isinstance(self.source_stats, Unset):
            source_stats = UNSET
        elif isinstance(self.source_stats, ProjectSourcesCollectionStats):
            source_stats = self.source_stats.to_dict()
        else:
            source_stats = self.source_stats

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "status": status,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if source_stats is not UNSET:
            field_dict["source_stats"] = source_stats

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action import Action
        from ..models.project_sources_collection_stats import ProjectSourcesCollectionStats

        d = dict(src_dict)
        action = Action.from_dict(d.pop("action"))

        status = ExecutionStatus(d.pop("status"))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_source_stats(data: object) -> Union["ProjectSourcesCollectionStats", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_stats_type_0 = ProjectSourcesCollectionStats.from_dict(data)

                return source_stats_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ProjectSourcesCollectionStats", None, Unset], data)

        source_stats = _parse_source_stats(d.pop("source_stats", UNSET))

        workflow_action_execution_metadata = cls(
            action=action,
            status=status,
            error_message=error_message,
            source_stats=source_stats,
        )

        workflow_action_execution_metadata.additional_properties = d
        return workflow_action_execution_metadata

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
