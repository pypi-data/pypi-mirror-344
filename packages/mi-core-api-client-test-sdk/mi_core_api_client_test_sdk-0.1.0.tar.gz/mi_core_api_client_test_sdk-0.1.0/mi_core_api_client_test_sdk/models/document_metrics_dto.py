from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric import Metric

if TYPE_CHECKING:
    from ..models.base_metric_dto import BaseMetricDTO


T = TypeVar("T", bound="DocumentMetricsDTO")


@_attrs_define
class DocumentMetricsDTO:
    """
    Attributes:
        document_id (UUID):
        metric (Metric): Enumeration class representing metrics.

            Attributes:
                UPVOTES: Represents upvotes metric.
                COMMENTS_COUNT: Represents comments count metric.
                VIEWS: Represents views metric.
                LIKES: Represents likes metric.
                SUBSCRIBERS: Represents subscribers metric.
                TOTAL_VIEWS: Represents total views metric.
                ONLINE_MEMBERS: Represents online members metric.
                MEMBERS: Represents members metric.
                RANK: Represents rank metric.
                BODY: Represents body metric.
                TITLE: Represents title metric.
                EST_REV : Represents estimated revenue metric.
                TOTAL_VIDEOS: Represents total videos metric.
                POSTS_COUNT: Represents posts count metric.
                POSTS_COMMENTS_COUNT: Represents posts comments count metric.
                POSTS_UPVOTES: Represents posts upvotes metric.
        metrics (list['BaseMetricDTO']):
    """

    document_id: UUID
    metric: Metric
    metrics: list["BaseMetricDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        document_id = str(self.document_id)

        metric = self.metric.value

        metrics = []
        for metrics_item_data in self.metrics:
            metrics_item = metrics_item_data.to_dict()
            metrics.append(metrics_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentId": document_id,
                "metric": metric,
                "metrics": metrics,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_metric_dto import BaseMetricDTO

        d = dict(src_dict)
        document_id = UUID(d.pop("documentId"))

        metric = Metric(d.pop("metric"))

        metrics = []
        _metrics = d.pop("metrics")
        for metrics_item_data in _metrics:
            metrics_item = BaseMetricDTO.from_dict(metrics_item_data)

            metrics.append(metrics_item)

        document_metrics_dto = cls(
            document_id=document_id,
            metric=metric,
            metrics=metrics,
        )

        document_metrics_dto.additional_properties = d
        return document_metrics_dto

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
