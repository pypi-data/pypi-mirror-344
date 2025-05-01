from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.youtube_channels_request_serp_results import YoutubeChannelsRequestSerpResults


T = TypeVar("T", bound="YoutubeChannelsRequest")


@_attrs_define
class YoutubeChannelsRequest:
    """
    Attributes:
        serp_results (YoutubeChannelsRequestSerpResults):
    """

    serp_results: "YoutubeChannelsRequestSerpResults"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        serp_results = self.serp_results.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "serp_results": serp_results,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.youtube_channels_request_serp_results import YoutubeChannelsRequestSerpResults

        d = dict(src_dict)
        serp_results = YoutubeChannelsRequestSerpResults.from_dict(d.pop("serp_results"))

        youtube_channels_request = cls(
            serp_results=serp_results,
        )

        youtube_channels_request.additional_properties = d
        return youtube_channels_request

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
