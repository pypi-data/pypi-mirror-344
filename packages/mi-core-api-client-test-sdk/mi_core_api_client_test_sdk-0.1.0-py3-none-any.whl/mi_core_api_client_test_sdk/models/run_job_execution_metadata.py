import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.execution_status import ExecutionStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RunJobExecutionMetadata")


@_attrs_define
class RunJobExecutionMetadata:
    """
    Attributes:
        execution_id (str):
        status (ExecutionStatus): Enumeration class representing workflow execution statuses.

            Attributes:
                INITIALIZED: Represents initialized job status.
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
                TERMINATED: Represents terminated job status.
        start_time (datetime.datetime):
        end_time (Union[None, Unset, datetime.datetime]):
        error_message (Union[None, Unset, str]):
    """

    execution_id: str
    status: ExecutionStatus
    start_time: datetime.datetime
    end_time: Union[None, Unset, datetime.datetime] = UNSET
    error_message: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_id = self.execution_id

        status = self.status.value

        start_time = self.start_time.isoformat()

        end_time: Union[None, Unset, str]
        if isinstance(self.end_time, Unset):
            end_time = UNSET
        elif isinstance(self.end_time, datetime.datetime):
            end_time = self.end_time.isoformat()
        else:
            end_time = self.end_time

        error_message: Union[None, Unset, str]
        if isinstance(self.error_message, Unset):
            error_message = UNSET
        else:
            error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "execution_id": execution_id,
                "status": status,
                "start_time": start_time,
            }
        )
        if end_time is not UNSET:
            field_dict["end_time"] = end_time
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        execution_id = d.pop("execution_id")

        status = ExecutionStatus(d.pop("status"))

        start_time = isoparse(d.pop("start_time"))

        def _parse_end_time(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_time_type_0 = isoparse(data)

                return end_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        end_time = _parse_end_time(d.pop("end_time", UNSET))

        def _parse_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        run_job_execution_metadata = cls(
            execution_id=execution_id,
            status=status,
            start_time=start_time,
            end_time=end_time,
            error_message=error_message,
        )

        run_job_execution_metadata.additional_properties = d
        return run_job_execution_metadata

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
