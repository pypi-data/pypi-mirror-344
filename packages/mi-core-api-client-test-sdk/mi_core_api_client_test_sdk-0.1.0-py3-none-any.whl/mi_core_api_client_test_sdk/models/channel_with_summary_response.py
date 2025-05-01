from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.youtube_video_optimize_with_id_schema import YoutubeVideoOptimizeWithIdSchema


T = TypeVar("T", bound="ChannelWithSummaryResponse")


@_attrs_define
class ChannelWithSummaryResponse:
    """
    Attributes:
        name (str):
        video_summary (YoutubeVideoOptimizeWithIdSchema):
        id (Union[Unset, UUID]):
    """

    name: str
    video_summary: "YoutubeVideoOptimizeWithIdSchema"
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        video_summary = self.video_summary.to_dict()

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "videoSummary": video_summary,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.youtube_video_optimize_with_id_schema import YoutubeVideoOptimizeWithIdSchema

        d = dict(src_dict)
        name = d.pop("name")

        video_summary = YoutubeVideoOptimizeWithIdSchema.from_dict(d.pop("videoSummary"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        channel_with_summary_response = cls(
            name=name,
            video_summary=video_summary,
            id=id,
        )

        channel_with_summary_response.additional_properties = d
        return channel_with_summary_response

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
