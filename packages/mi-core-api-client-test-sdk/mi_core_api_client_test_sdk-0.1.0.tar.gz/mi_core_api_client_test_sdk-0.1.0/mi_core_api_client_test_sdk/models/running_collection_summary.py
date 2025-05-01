from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.article_summary import ArticleSummary
    from ..models.overall_summary import OverallSummary
    from ..models.reddit_summary import RedditSummary
    from ..models.youtube_summary import YoutubeSummary


T = TypeVar("T", bound="RunningCollectionSummary")


@_attrs_define
class RunningCollectionSummary:
    """
    Attributes:
        overall (Union['OverallSummary', None]):
        reddit (Union['RedditSummary', None]):
        youtube (Union['YoutubeSummary', None]):
        article (Union['ArticleSummary', None]):
    """

    overall: Union["OverallSummary", None]
    reddit: Union["RedditSummary", None]
    youtube: Union["YoutubeSummary", None]
    article: Union["ArticleSummary", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.article_summary import ArticleSummary
        from ..models.overall_summary import OverallSummary
        from ..models.reddit_summary import RedditSummary
        from ..models.youtube_summary import YoutubeSummary

        overall: Union[None, dict[str, Any]]
        if isinstance(self.overall, OverallSummary):
            overall = self.overall.to_dict()
        else:
            overall = self.overall

        reddit: Union[None, dict[str, Any]]
        if isinstance(self.reddit, RedditSummary):
            reddit = self.reddit.to_dict()
        else:
            reddit = self.reddit

        youtube: Union[None, dict[str, Any]]
        if isinstance(self.youtube, YoutubeSummary):
            youtube = self.youtube.to_dict()
        else:
            youtube = self.youtube

        article: Union[None, dict[str, Any]]
        if isinstance(self.article, ArticleSummary):
            article = self.article.to_dict()
        else:
            article = self.article

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "overall": overall,
                "reddit": reddit,
                "youtube": youtube,
                "article": article,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_summary import ArticleSummary
        from ..models.overall_summary import OverallSummary
        from ..models.reddit_summary import RedditSummary
        from ..models.youtube_summary import YoutubeSummary

        d = dict(src_dict)

        def _parse_overall(data: object) -> Union["OverallSummary", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                overall_type_0 = OverallSummary.from_dict(data)

                return overall_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OverallSummary", None], data)

        overall = _parse_overall(d.pop("overall"))

        def _parse_reddit(data: object) -> Union["RedditSummary", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                reddit_type_0 = RedditSummary.from_dict(data)

                return reddit_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RedditSummary", None], data)

        reddit = _parse_reddit(d.pop("reddit"))

        def _parse_youtube(data: object) -> Union["YoutubeSummary", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                youtube_type_0 = YoutubeSummary.from_dict(data)

                return youtube_type_0
            except:  # noqa: E722
                pass
            return cast(Union["YoutubeSummary", None], data)

        youtube = _parse_youtube(d.pop("youtube"))

        def _parse_article(data: object) -> Union["ArticleSummary", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                article_type_0 = ArticleSummary.from_dict(data)

                return article_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ArticleSummary", None], data)

        article = _parse_article(d.pop("article"))

        running_collection_summary = cls(
            overall=overall,
            reddit=reddit,
            youtube=youtube,
            article=article,
        )

        running_collection_summary.additional_properties = d
        return running_collection_summary

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
