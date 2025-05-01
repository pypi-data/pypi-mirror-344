from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.source_types import SourceTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.articles_params import ArticlesParams
    from ..models.articles_search_params import ArticlesSearchParams
    from ..models.reddit_post_params import RedditPostParams
    from ..models.reddit_search_params import RedditSearchParams
    from ..models.reddit_user_params import RedditUserParams
    from ..models.sub_reddit_params import SubRedditParams
    from ..models.youtube_channel_params import YoutubeChannelParams
    from ..models.youtube_search_params import YoutubeSearchParams
    from ..models.youtube_video_params import YoutubeVideoParams


T = TypeVar("T", bound="SourceCreateManySchema")


@_attrs_define
class SourceCreateManySchema:
    """
    Attributes:
        source_type (SourceTypes): Enumeration class representing source types.
        params (Union['ArticlesParams', 'ArticlesSearchParams', 'RedditPostParams', 'RedditSearchParams',
            'RedditUserParams', 'SubRedditParams', 'YoutubeChannelParams', 'YoutubeSearchParams', 'YoutubeVideoParams']):
        input_urls (Union[Unset, list[str]]):
        input_queries (Union[Unset, list[str]]):
        collection_ids (Union[None, Unset, list[UUID]]):
        project_ids (Union[None, Unset, list[UUID]]):
    """

    source_type: SourceTypes
    params: Union[
        "ArticlesParams",
        "ArticlesSearchParams",
        "RedditPostParams",
        "RedditSearchParams",
        "RedditUserParams",
        "SubRedditParams",
        "YoutubeChannelParams",
        "YoutubeSearchParams",
        "YoutubeVideoParams",
    ]
    input_urls: Union[Unset, list[str]] = UNSET
    input_queries: Union[Unset, list[str]] = UNSET
    collection_ids: Union[None, Unset, list[UUID]] = UNSET
    project_ids: Union[None, Unset, list[UUID]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.articles_params import ArticlesParams
        from ..models.reddit_post_params import RedditPostParams
        from ..models.reddit_search_params import RedditSearchParams
        from ..models.reddit_user_params import RedditUserParams
        from ..models.sub_reddit_params import SubRedditParams
        from ..models.youtube_channel_params import YoutubeChannelParams
        from ..models.youtube_search_params import YoutubeSearchParams
        from ..models.youtube_video_params import YoutubeVideoParams

        source_type = self.source_type.value

        params: dict[str, Any]
        if isinstance(self.params, YoutubeChannelParams):
            params = self.params.to_dict()
        elif isinstance(self.params, YoutubeSearchParams):
            params = self.params.to_dict()
        elif isinstance(self.params, YoutubeVideoParams):
            params = self.params.to_dict()
        elif isinstance(self.params, SubRedditParams):
            params = self.params.to_dict()
        elif isinstance(self.params, RedditUserParams):
            params = self.params.to_dict()
        elif isinstance(self.params, RedditSearchParams):
            params = self.params.to_dict()
        elif isinstance(self.params, RedditPostParams):
            params = self.params.to_dict()
        elif isinstance(self.params, ArticlesParams):
            params = self.params.to_dict()
        else:
            params = self.params.to_dict()

        input_urls: Union[Unset, list[str]] = UNSET
        if not isinstance(self.input_urls, Unset):
            input_urls = self.input_urls

        input_queries: Union[Unset, list[str]] = UNSET
        if not isinstance(self.input_queries, Unset):
            input_queries = self.input_queries

        collection_ids: Union[None, Unset, list[str]]
        if isinstance(self.collection_ids, Unset):
            collection_ids = UNSET
        elif isinstance(self.collection_ids, list):
            collection_ids = []
            for collection_ids_type_0_item_data in self.collection_ids:
                collection_ids_type_0_item = str(collection_ids_type_0_item_data)
                collection_ids.append(collection_ids_type_0_item)

        else:
            collection_ids = self.collection_ids

        project_ids: Union[None, Unset, list[str]]
        if isinstance(self.project_ids, Unset):
            project_ids = UNSET
        elif isinstance(self.project_ids, list):
            project_ids = []
            for project_ids_type_0_item_data in self.project_ids:
                project_ids_type_0_item = str(project_ids_type_0_item_data)
                project_ids.append(project_ids_type_0_item)

        else:
            project_ids = self.project_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_type": source_type,
                "params": params,
            }
        )
        if input_urls is not UNSET:
            field_dict["input_urls"] = input_urls
        if input_queries is not UNSET:
            field_dict["input_queries"] = input_queries
        if collection_ids is not UNSET:
            field_dict["collection_ids"] = collection_ids
        if project_ids is not UNSET:
            field_dict["project_ids"] = project_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.articles_params import ArticlesParams
        from ..models.articles_search_params import ArticlesSearchParams
        from ..models.reddit_post_params import RedditPostParams
        from ..models.reddit_search_params import RedditSearchParams
        from ..models.reddit_user_params import RedditUserParams
        from ..models.sub_reddit_params import SubRedditParams
        from ..models.youtube_channel_params import YoutubeChannelParams
        from ..models.youtube_search_params import YoutubeSearchParams
        from ..models.youtube_video_params import YoutubeVideoParams

        d = dict(src_dict)
        source_type = SourceTypes(d.pop("source_type"))

        def _parse_params(
            data: object,
        ) -> Union[
            "ArticlesParams",
            "ArticlesSearchParams",
            "RedditPostParams",
            "RedditSearchParams",
            "RedditUserParams",
            "SubRedditParams",
            "YoutubeChannelParams",
            "YoutubeSearchParams",
            "YoutubeVideoParams",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_0 = YoutubeChannelParams.from_dict(data)

                return params_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_1 = YoutubeSearchParams.from_dict(data)

                return params_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_2 = YoutubeVideoParams.from_dict(data)

                return params_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_3 = SubRedditParams.from_dict(data)

                return params_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_4 = RedditUserParams.from_dict(data)

                return params_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_5 = RedditSearchParams.from_dict(data)

                return params_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_6 = RedditPostParams.from_dict(data)

                return params_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_7 = ArticlesParams.from_dict(data)

                return params_type_7
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            params_type_8 = ArticlesSearchParams.from_dict(data)

            return params_type_8

        params = _parse_params(d.pop("params"))

        input_urls = cast(list[str], d.pop("input_urls", UNSET))

        input_queries = cast(list[str], d.pop("input_queries", UNSET))

        def _parse_collection_ids(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                collection_ids_type_0 = []
                _collection_ids_type_0 = data
                for collection_ids_type_0_item_data in _collection_ids_type_0:
                    collection_ids_type_0_item = UUID(collection_ids_type_0_item_data)

                    collection_ids_type_0.append(collection_ids_type_0_item)

                return collection_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        collection_ids = _parse_collection_ids(d.pop("collection_ids", UNSET))

        def _parse_project_ids(data: object) -> Union[None, Unset, list[UUID]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                project_ids_type_0 = []
                _project_ids_type_0 = data
                for project_ids_type_0_item_data in _project_ids_type_0:
                    project_ids_type_0_item = UUID(project_ids_type_0_item_data)

                    project_ids_type_0.append(project_ids_type_0_item)

                return project_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[UUID]], data)

        project_ids = _parse_project_ids(d.pop("project_ids", UNSET))

        source_create_many_schema = cls(
            source_type=source_type,
            params=params,
            input_urls=input_urls,
            input_queries=input_queries,
            collection_ids=collection_ids,
            project_ids=project_ids,
        )

        source_create_many_schema.additional_properties = d
        return source_create_many_schema

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
