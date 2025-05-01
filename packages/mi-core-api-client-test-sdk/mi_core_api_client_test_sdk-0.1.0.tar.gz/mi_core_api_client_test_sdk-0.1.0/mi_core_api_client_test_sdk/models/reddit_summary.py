import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RedditSummary")


@_attrs_define
class RedditSummary:
    """
    Attributes:
        documents_count (int):
        last_updated (datetime.datetime):
        avg_karma (float):
        active_users (int):
    """

    documents_count: int
    last_updated: datetime.datetime
    avg_karma: float
    active_users: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        documents_count = self.documents_count

        last_updated = self.last_updated.isoformat()

        avg_karma = self.avg_karma

        active_users = self.active_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documentsCount": documents_count,
                "lastUpdated": last_updated,
                "avgKarma": avg_karma,
                "activeUsers": active_users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        documents_count = d.pop("documentsCount")

        last_updated = isoparse(d.pop("lastUpdated"))

        avg_karma = d.pop("avgKarma")

        active_users = d.pop("activeUsers")

        reddit_summary = cls(
            documents_count=documents_count,
            last_updated=last_updated,
            avg_karma=avg_karma,
            active_users=active_users,
        )

        reddit_summary.additional_properties = d
        return reddit_summary

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
