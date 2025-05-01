from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="YoutubeChannelsWithVideosIdsFromDB")


@_attrs_define
class YoutubeChannelsWithVideosIdsFromDB:
    """
    Attributes:
        channel_id (UUID):
        video_ids (list[UUID]):
    """

    channel_id: UUID
    video_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        channel_id = str(self.channel_id)

        video_ids = []
        for video_ids_item_data in self.video_ids:
            video_ids_item = str(video_ids_item_data)
            video_ids.append(video_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channel_id": channel_id,
                "video_ids": video_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        channel_id = UUID(d.pop("channel_id"))

        video_ids = []
        _video_ids = d.pop("video_ids")
        for video_ids_item_data in _video_ids:
            video_ids_item = UUID(video_ids_item_data)

            video_ids.append(video_ids_item)

        youtube_channels_with_videos_ids_from_db = cls(
            channel_id=channel_id,
            video_ids=video_ids,
        )

        youtube_channels_with_videos_ids_from_db.additional_properties = d
        return youtube_channels_with_videos_ids_from_db

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
