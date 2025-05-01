from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.channel import Channel


T = TypeVar("T", bound="YoutubeVideoWithChannel")


@_attrs_define
class YoutubeVideoWithChannel:
    """
    Attributes:
        title (str):
        channel_link (str):
        body (str):
        views (int):
        likes (int):
        length (str):
        id (Union[Unset, UUID]):
        channel (Union['Channel', None, Unset]):
    """

    title: str
    channel_link: str
    body: str
    views: int
    likes: int
    length: str
    id: Union[Unset, UUID] = UNSET
    channel: Union["Channel", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.channel import Channel

        title = self.title

        channel_link = self.channel_link

        body = self.body

        views = self.views

        likes = self.likes

        length = self.length

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        channel: Union[None, Unset, dict[str, Any]]
        if isinstance(self.channel, Unset):
            channel = UNSET
        elif isinstance(self.channel, Channel):
            channel = self.channel.to_dict()
        else:
            channel = self.channel

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "channelLink": channel_link,
                "body": body,
                "views": views,
                "likes": likes,
                "length": length,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if channel is not UNSET:
            field_dict["channel"] = channel

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.channel import Channel

        d = dict(src_dict)
        title = d.pop("title")

        channel_link = d.pop("channelLink")

        body = d.pop("body")

        views = d.pop("views")

        likes = d.pop("likes")

        length = d.pop("length")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        def _parse_channel(data: object) -> Union["Channel", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                channel_type_0 = Channel.from_dict(data)

                return channel_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Channel", None, Unset], data)

        channel = _parse_channel(d.pop("channel", UNSET))

        youtube_video_with_channel = cls(
            title=title,
            channel_link=channel_link,
            body=body,
            views=views,
            likes=likes,
            length=length,
            id=id,
            channel=channel,
        )

        youtube_video_with_channel.additional_properties = d
        return youtube_video_with_channel

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
