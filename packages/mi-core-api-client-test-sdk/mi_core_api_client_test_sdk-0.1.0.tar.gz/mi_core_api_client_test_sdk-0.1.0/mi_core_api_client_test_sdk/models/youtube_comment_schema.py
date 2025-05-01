import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeCommentSchema")


@_attrs_define
class YoutubeCommentSchema:
    """
    Attributes:
        body (Union[None, str]):
        topic_id (UUID):
        published_date (datetime.date):
        author (str):
        likes (int):
        reply_count (int):
        id (Union[Unset, UUID]):
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
        video_id (Union[None, UUID, Unset]):
        is_available (Union[Unset, bool]):  Default: True.
    """

    body: Union[None, str]
    topic_id: UUID
    published_date: datetime.date
    author: str
    likes: int
    reply_count: int
    id: Union[Unset, UUID] = UNSET
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    video_id: Union[None, UUID, Unset] = UNSET
    is_available: Union[Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body: Union[None, str]
        body = self.body

        topic_id = str(self.topic_id)

        published_date = self.published_date.isoformat()

        author = self.author

        likes = self.likes

        reply_count = self.reply_count

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        video_id: Union[None, Unset, str]
        if isinstance(self.video_id, Unset):
            video_id = UNSET
        elif isinstance(self.video_id, UUID):
            video_id = str(self.video_id)
        else:
            video_id = self.video_id

        is_available = self.is_available

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "topicId": topic_id,
                "publishedDate": published_date,
                "author": author,
                "likes": likes,
                "replyCount": reply_count,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if video_id is not UNSET:
            field_dict["videoId"] = video_id
        if is_available is not UNSET:
            field_dict["isAvailable"] = is_available

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

        topic_id = UUID(d.pop("topicId"))

        published_date = isoparse(d.pop("publishedDate")).date()

        author = d.pop("author")

        likes = d.pop("likes")

        reply_count = d.pop("replyCount")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        def _parse_video_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                video_id_type_0 = UUID(data)

                return video_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        video_id = _parse_video_id(d.pop("videoId", UNSET))

        is_available = d.pop("isAvailable", UNSET)

        youtube_comment_schema = cls(
            body=body,
            topic_id=topic_id,
            published_date=published_date,
            author=author,
            likes=likes,
            reply_count=reply_count,
            id=id,
            updated_at=updated_at,
            video_id=video_id,
            is_available=is_available,
        )

        youtube_comment_schema.additional_properties = d
        return youtube_comment_schema

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
