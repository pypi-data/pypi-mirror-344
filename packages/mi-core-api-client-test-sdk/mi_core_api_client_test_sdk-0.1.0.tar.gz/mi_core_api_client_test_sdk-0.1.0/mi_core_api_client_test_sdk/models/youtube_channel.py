from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeChannel")


@_attrs_define
class YoutubeChannel:
    """
    Attributes:
        title (str):
        body (str):
        subscribers (int):
        total_views (int):
        total_videos (int):
        id (Union[Unset, UUID]):
    """

    title: str
    body: str
    subscribers: int
    total_views: int
    total_videos: int
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        body = self.body

        subscribers = self.subscribers

        total_views = self.total_views

        total_videos = self.total_videos

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "body": body,
                "subscribers": subscribers,
                "totalViews": total_views,
                "totalVideos": total_videos,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        body = d.pop("body")

        subscribers = d.pop("subscribers")

        total_views = d.pop("totalViews")

        total_videos = d.pop("totalVideos")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        youtube_channel = cls(
            title=title,
            body=body,
            subscribers=subscribers,
            total_views=total_views,
            total_videos=total_videos,
            id=id,
        )

        youtube_channel.additional_properties = d
        return youtube_channel

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
