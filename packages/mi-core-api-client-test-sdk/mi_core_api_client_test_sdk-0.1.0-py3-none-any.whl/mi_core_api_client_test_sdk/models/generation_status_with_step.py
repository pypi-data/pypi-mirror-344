import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_generation_step_enum import ContentGenerationStepEnum
from ..models.storyboard_generation_status_enum import StoryboardGenerationStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.channel_content_summary_response import ChannelContentSummaryResponse
    from ..models.collect_serp_data import CollectSerpData
    from ..models.collect_youtube_channels_data import CollectYoutubeChannelsData
    from ..models.collect_youtube_videos_data import CollectYoutubeVideosData
    from ..models.related_topics_data import RelatedTopicsData
    from ..models.storyboard_content_response import StoryboardContentResponse
    from ..models.storyboard_restrictions_response import StoryboardRestrictionsResponse
    from ..models.storyboard_seed_keywords_response import StoryboardSeedKeywordsResponse
    from ..models.video_coverage_response import VideoCoverageResponse


T = TypeVar("T", bound="GenerationStatusWithStep")


@_attrs_define
class GenerationStatusWithStep:
    """
    Attributes:
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        status (StoryboardGenerationStatusEnum): Enumeration class representing storyboard generation status.
        step (ContentGenerationStepEnum): Enumeration class representing content generation steps.
        data (Union['ChannelContentSummaryResponse', 'CollectSerpData', 'CollectYoutubeChannelsData',
            'CollectYoutubeVideosData', 'RelatedTopicsData', 'StoryboardContentResponse', 'StoryboardRestrictionsResponse',
            'StoryboardSeedKeywordsResponse', 'VideoCoverageResponse', None, Unset]):
    """

    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: StoryboardGenerationStatusEnum
    step: ContentGenerationStepEnum
    data: Union[
        "ChannelContentSummaryResponse",
        "CollectSerpData",
        "CollectYoutubeChannelsData",
        "CollectYoutubeVideosData",
        "RelatedTopicsData",
        "StoryboardContentResponse",
        "StoryboardRestrictionsResponse",
        "StoryboardSeedKeywordsResponse",
        "VideoCoverageResponse",
        None,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.channel_content_summary_response import ChannelContentSummaryResponse
        from ..models.collect_serp_data import CollectSerpData
        from ..models.collect_youtube_channels_data import CollectYoutubeChannelsData
        from ..models.collect_youtube_videos_data import CollectYoutubeVideosData
        from ..models.related_topics_data import RelatedTopicsData
        from ..models.storyboard_content_response import StoryboardContentResponse
        from ..models.storyboard_restrictions_response import StoryboardRestrictionsResponse
        from ..models.storyboard_seed_keywords_response import StoryboardSeedKeywordsResponse
        from ..models.video_coverage_response import VideoCoverageResponse

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status = self.status.value

        step = self.step.value

        data: Union[None, Unset, dict[str, Any]]
        if isinstance(self.data, Unset):
            data = UNSET
        elif isinstance(self.data, RelatedTopicsData):
            data = self.data.to_dict()
        elif isinstance(self.data, CollectSerpData):
            data = self.data.to_dict()
        elif isinstance(self.data, CollectYoutubeChannelsData):
            data = self.data.to_dict()
        elif isinstance(self.data, CollectYoutubeVideosData):
            data = self.data.to_dict()
        elif isinstance(self.data, VideoCoverageResponse):
            data = self.data.to_dict()
        elif isinstance(self.data, ChannelContentSummaryResponse):
            data = self.data.to_dict()
        elif isinstance(self.data, StoryboardSeedKeywordsResponse):
            data = self.data.to_dict()
        elif isinstance(self.data, StoryboardRestrictionsResponse):
            data = self.data.to_dict()
        elif isinstance(self.data, StoryboardContentResponse):
            data = self.data.to_dict()
        else:
            data = self.data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "createdAt": created_at,
                "updatedAt": updated_at,
                "status": status,
                "step": step,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.channel_content_summary_response import ChannelContentSummaryResponse
        from ..models.collect_serp_data import CollectSerpData
        from ..models.collect_youtube_channels_data import CollectYoutubeChannelsData
        from ..models.collect_youtube_videos_data import CollectYoutubeVideosData
        from ..models.related_topics_data import RelatedTopicsData
        from ..models.storyboard_content_response import StoryboardContentResponse
        from ..models.storyboard_restrictions_response import StoryboardRestrictionsResponse
        from ..models.storyboard_seed_keywords_response import StoryboardSeedKeywordsResponse
        from ..models.video_coverage_response import VideoCoverageResponse

        d = dict(src_dict)
        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        status = StoryboardGenerationStatusEnum(d.pop("status"))

        step = ContentGenerationStepEnum(d.pop("step"))

        def _parse_data(
            data: object,
        ) -> Union[
            "ChannelContentSummaryResponse",
            "CollectSerpData",
            "CollectYoutubeChannelsData",
            "CollectYoutubeVideosData",
            "RelatedTopicsData",
            "StoryboardContentResponse",
            "StoryboardRestrictionsResponse",
            "StoryboardSeedKeywordsResponse",
            "VideoCoverageResponse",
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = RelatedTopicsData.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_1 = CollectSerpData.from_dict(data)

                return data_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_2 = CollectYoutubeChannelsData.from_dict(data)

                return data_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_3 = CollectYoutubeVideosData.from_dict(data)

                return data_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_4 = VideoCoverageResponse.from_dict(data)

                return data_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_5 = ChannelContentSummaryResponse.from_dict(data)

                return data_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_6 = StoryboardSeedKeywordsResponse.from_dict(data)

                return data_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_7 = StoryboardRestrictionsResponse.from_dict(data)

                return data_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_8 = StoryboardContentResponse.from_dict(data)

                return data_type_8
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "ChannelContentSummaryResponse",
                    "CollectSerpData",
                    "CollectYoutubeChannelsData",
                    "CollectYoutubeVideosData",
                    "RelatedTopicsData",
                    "StoryboardContentResponse",
                    "StoryboardRestrictionsResponse",
                    "StoryboardSeedKeywordsResponse",
                    "VideoCoverageResponse",
                    None,
                    Unset,
                ],
                data,
            )

        data = _parse_data(d.pop("data", UNSET))

        generation_status_with_step = cls(
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            step=step,
            data=data,
        )

        generation_status_with_step.additional_properties = d
        return generation_status_with_step

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
