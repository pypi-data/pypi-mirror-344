from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="YoutubeVideoOptimizeWithIdSchema")


@_attrs_define
class YoutubeVideoOptimizeWithIdSchema:
    """
    Attributes:
        title (str):
        length (str):
        body (str):
        category (Union[None, str]):
        language (str):
        transcript (Union[None, Unset, str]):
        id (Union[Unset, UUID]):
    """

    title: str
    length: str
    body: str
    category: Union[None, str]
    language: str
    transcript: Union[None, Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        length = self.length

        body = self.body

        category: Union[None, str]
        category = self.category

        language = self.language

        transcript: Union[None, Unset, str]
        if isinstance(self.transcript, Unset):
            transcript = UNSET
        else:
            transcript = self.transcript

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "length": length,
                "body": body,
                "category": category,
                "language": language,
            }
        )
        if transcript is not UNSET:
            field_dict["transcript"] = transcript
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        length = d.pop("length")

        body = d.pop("body")

        def _parse_category(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category = _parse_category(d.pop("category"))

        language = d.pop("language")

        def _parse_transcript(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        transcript = _parse_transcript(d.pop("transcript", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        youtube_video_optimize_with_id_schema = cls(
            title=title,
            length=length,
            body=body,
            category=category,
            language=language,
            transcript=transcript,
            id=id,
        )

        youtube_video_optimize_with_id_schema.additional_properties = d
        return youtube_video_optimize_with_id_schema

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
