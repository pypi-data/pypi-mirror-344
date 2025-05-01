from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.collect_youtube_videos_data_youtubevideos import CollectYoutubeVideosDataYoutubevideos


T = TypeVar("T", bound="CollectYoutubeVideosData")


@_attrs_define
class CollectYoutubeVideosData:
    """
    Attributes:
        youtube_videos (CollectYoutubeVideosDataYoutubevideos):
    """

    youtube_videos: "CollectYoutubeVideosDataYoutubevideos"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_videos = self.youtube_videos.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "youtubeVideos": youtube_videos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.collect_youtube_videos_data_youtubevideos import CollectYoutubeVideosDataYoutubevideos

        d = dict(src_dict)
        youtube_videos = CollectYoutubeVideosDataYoutubevideos.from_dict(d.pop("youtubeVideos"))

        collect_youtube_videos_data = cls(
            youtube_videos=youtube_videos,
        )

        collect_youtube_videos_data.additional_properties = d
        return collect_youtube_videos_data

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
