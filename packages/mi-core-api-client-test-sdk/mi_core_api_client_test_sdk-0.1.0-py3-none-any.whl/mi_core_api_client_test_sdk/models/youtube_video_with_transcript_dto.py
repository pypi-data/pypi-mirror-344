from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.youtube_video_schema import YoutubeVideoSchema
    from ..models.youtube_video_transcript_schema import YoutubeVideoTranscriptSchema


T = TypeVar("T", bound="YoutubeVideoWithTranscriptDTO")


@_attrs_define
class YoutubeVideoWithTranscriptDTO:
    """
    Attributes:
        video (YoutubeVideoSchema):
        transcript (Union['YoutubeVideoTranscriptSchema', None, Unset]):
    """

    video: "YoutubeVideoSchema"
    transcript: Union["YoutubeVideoTranscriptSchema", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.youtube_video_transcript_schema import YoutubeVideoTranscriptSchema

        video = self.video.to_dict()

        transcript: Union[None, Unset, dict[str, Any]]
        if isinstance(self.transcript, Unset):
            transcript = UNSET
        elif isinstance(self.transcript, YoutubeVideoTranscriptSchema):
            transcript = self.transcript.to_dict()
        else:
            transcript = self.transcript

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "video": video,
            }
        )
        if transcript is not UNSET:
            field_dict["transcript"] = transcript

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.youtube_video_schema import YoutubeVideoSchema
        from ..models.youtube_video_transcript_schema import YoutubeVideoTranscriptSchema

        d = dict(src_dict)
        video = YoutubeVideoSchema.from_dict(d.pop("video"))

        def _parse_transcript(data: object) -> Union["YoutubeVideoTranscriptSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                transcript_type_0 = YoutubeVideoTranscriptSchema.from_dict(data)

                return transcript_type_0
            except:  # noqa: E722
                pass
            return cast(Union["YoutubeVideoTranscriptSchema", None, Unset], data)

        transcript = _parse_transcript(d.pop("transcript", UNSET))

        youtube_video_with_transcript_dto = cls(
            video=video,
            transcript=transcript,
        )

        youtube_video_with_transcript_dto.additional_properties = d
        return youtube_video_with_transcript_dto

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
