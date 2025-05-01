from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_status_response import ProjectStatusResponse


T = TypeVar("T", bound="ProjectStatusSummaryResponse")


@_attrs_define
class ProjectStatusSummaryResponse:
    """
    Attributes:
        metadata_status (ProjectStatusResponse):
        data_status (ProjectStatusResponse):
        report_status (ProjectStatusResponse):
    """

    metadata_status: "ProjectStatusResponse"
    data_status: "ProjectStatusResponse"
    report_status: "ProjectStatusResponse"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata_status = self.metadata_status.to_dict()

        data_status = self.data_status.to_dict()

        report_status = self.report_status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadataStatus": metadata_status,
                "dataStatus": data_status,
                "reportStatus": report_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_status_response import ProjectStatusResponse

        d = dict(src_dict)
        metadata_status = ProjectStatusResponse.from_dict(d.pop("metadataStatus"))

        data_status = ProjectStatusResponse.from_dict(d.pop("dataStatus"))

        report_status = ProjectStatusResponse.from_dict(d.pop("reportStatus"))

        project_status_summary_response = cls(
            metadata_status=metadata_status,
            data_status=data_status,
            report_status=report_status,
        )

        project_status_summary_response.additional_properties = d
        return project_status_summary_response

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
