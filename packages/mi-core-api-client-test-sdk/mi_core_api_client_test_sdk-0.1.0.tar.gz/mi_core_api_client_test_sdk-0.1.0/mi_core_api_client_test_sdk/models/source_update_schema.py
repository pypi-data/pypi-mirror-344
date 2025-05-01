from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.source_types import SourceTypes

if TYPE_CHECKING:
    from ..models.partial_articles_params import PartialArticlesParams
    from ..models.partial_articles_search_params import PartialArticlesSearchParams
    from ..models.partial_reddit_post_params import PartialRedditPostParams
    from ..models.partial_reddit_search_params import PartialRedditSearchParams
    from ..models.partial_reddit_user_params import PartialRedditUserParams
    from ..models.partial_sub_reddit_params import PartialSubRedditParams
    from ..models.partial_youtube_channel_params import PartialYoutubeChannelParams
    from ..models.partial_youtube_search_params import PartialYoutubeSearchParams
    from ..models.partial_youtube_video_params import PartialYoutubeVideoParams


T = TypeVar("T", bound="SourceUpdateSchema")


@_attrs_define
class SourceUpdateSchema:
    """
    Attributes:
        source_type (SourceTypes): Enumeration class representing source types.
        params (Union['PartialArticlesParams', 'PartialArticlesSearchParams', 'PartialRedditPostParams',
            'PartialRedditSearchParams', 'PartialRedditUserParams', 'PartialSubRedditParams', 'PartialYoutubeChannelParams',
            'PartialYoutubeSearchParams', 'PartialYoutubeVideoParams']):
        source_ids (list[UUID]):
    """

    source_type: SourceTypes
    params: Union[
        "PartialArticlesParams",
        "PartialArticlesSearchParams",
        "PartialRedditPostParams",
        "PartialRedditSearchParams",
        "PartialRedditUserParams",
        "PartialSubRedditParams",
        "PartialYoutubeChannelParams",
        "PartialYoutubeSearchParams",
        "PartialYoutubeVideoParams",
    ]
    source_ids: list[UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.partial_articles_params import PartialArticlesParams
        from ..models.partial_reddit_post_params import PartialRedditPostParams
        from ..models.partial_reddit_search_params import PartialRedditSearchParams
        from ..models.partial_reddit_user_params import PartialRedditUserParams
        from ..models.partial_sub_reddit_params import PartialSubRedditParams
        from ..models.partial_youtube_channel_params import PartialYoutubeChannelParams
        from ..models.partial_youtube_search_params import PartialYoutubeSearchParams
        from ..models.partial_youtube_video_params import PartialYoutubeVideoParams

        source_type = self.source_type.value

        params: dict[str, Any]
        if isinstance(self.params, PartialYoutubeChannelParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialYoutubeSearchParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialYoutubeVideoParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialSubRedditParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialRedditUserParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialRedditSearchParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialRedditPostParams):
            params = self.params.to_dict()
        elif isinstance(self.params, PartialArticlesParams):
            params = self.params.to_dict()
        else:
            params = self.params.to_dict()

        source_ids = []
        for source_ids_item_data in self.source_ids:
            source_ids_item = str(source_ids_item_data)
            source_ids.append(source_ids_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_type": source_type,
                "params": params,
                "source_ids": source_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.partial_articles_params import PartialArticlesParams
        from ..models.partial_articles_search_params import PartialArticlesSearchParams
        from ..models.partial_reddit_post_params import PartialRedditPostParams
        from ..models.partial_reddit_search_params import PartialRedditSearchParams
        from ..models.partial_reddit_user_params import PartialRedditUserParams
        from ..models.partial_sub_reddit_params import PartialSubRedditParams
        from ..models.partial_youtube_channel_params import PartialYoutubeChannelParams
        from ..models.partial_youtube_search_params import PartialYoutubeSearchParams
        from ..models.partial_youtube_video_params import PartialYoutubeVideoParams

        d = dict(src_dict)
        source_type = SourceTypes(d.pop("source_type"))

        def _parse_params(
            data: object,
        ) -> Union[
            "PartialArticlesParams",
            "PartialArticlesSearchParams",
            "PartialRedditPostParams",
            "PartialRedditSearchParams",
            "PartialRedditUserParams",
            "PartialSubRedditParams",
            "PartialYoutubeChannelParams",
            "PartialYoutubeSearchParams",
            "PartialYoutubeVideoParams",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_0 = PartialYoutubeChannelParams.from_dict(data)

                return params_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_1 = PartialYoutubeSearchParams.from_dict(data)

                return params_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_2 = PartialYoutubeVideoParams.from_dict(data)

                return params_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_3 = PartialSubRedditParams.from_dict(data)

                return params_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_4 = PartialRedditUserParams.from_dict(data)

                return params_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_5 = PartialRedditSearchParams.from_dict(data)

                return params_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_6 = PartialRedditPostParams.from_dict(data)

                return params_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_7 = PartialArticlesParams.from_dict(data)

                return params_type_7
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            params_type_8 = PartialArticlesSearchParams.from_dict(data)

            return params_type_8

        params = _parse_params(d.pop("params"))

        source_ids = []
        _source_ids = d.pop("source_ids")
        for source_ids_item_data in _source_ids:
            source_ids_item = UUID(source_ids_item_data)

            source_ids.append(source_ids_item)

        source_update_schema = cls(
            source_type=source_type,
            params=params,
            source_ids=source_ids,
        )

        source_update_schema.additional_properties = d
        return source_update_schema

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
