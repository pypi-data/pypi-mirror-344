from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.news_article import NewsArticle
    from ..models.reddit_post import RedditPost
    from ..models.you_tube_video import YouTubeVideo


T = TypeVar("T", bound="Coverage")


@_attrs_define
class Coverage:
    """
    Attributes:
        news_articles (list['NewsArticle']):
        youtube_videos (Union[None, Unset, list['YouTubeVideo']]):
        reddit_posts (Union[None, Unset, list['RedditPost']]):
    """

    news_articles: list["NewsArticle"]
    youtube_videos: Union[None, Unset, list["YouTubeVideo"]] = UNSET
    reddit_posts: Union[None, Unset, list["RedditPost"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        news_articles = []
        for news_articles_item_data in self.news_articles:
            news_articles_item = news_articles_item_data.to_dict()
            news_articles.append(news_articles_item)

        youtube_videos: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.youtube_videos, Unset):
            youtube_videos = UNSET
        elif isinstance(self.youtube_videos, list):
            youtube_videos = []
            for youtube_videos_type_0_item_data in self.youtube_videos:
                youtube_videos_type_0_item = youtube_videos_type_0_item_data.to_dict()
                youtube_videos.append(youtube_videos_type_0_item)

        else:
            youtube_videos = self.youtube_videos

        reddit_posts: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.reddit_posts, Unset):
            reddit_posts = UNSET
        elif isinstance(self.reddit_posts, list):
            reddit_posts = []
            for reddit_posts_type_0_item_data in self.reddit_posts:
                reddit_posts_type_0_item = reddit_posts_type_0_item_data.to_dict()
                reddit_posts.append(reddit_posts_type_0_item)

        else:
            reddit_posts = self.reddit_posts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "newsArticles": news_articles,
            }
        )
        if youtube_videos is not UNSET:
            field_dict["youtubeVideos"] = youtube_videos
        if reddit_posts is not UNSET:
            field_dict["redditPosts"] = reddit_posts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.news_article import NewsArticle
        from ..models.reddit_post import RedditPost
        from ..models.you_tube_video import YouTubeVideo

        d = dict(src_dict)
        news_articles = []
        _news_articles = d.pop("newsArticles")
        for news_articles_item_data in _news_articles:
            news_articles_item = NewsArticle.from_dict(news_articles_item_data)

            news_articles.append(news_articles_item)

        def _parse_youtube_videos(data: object) -> Union[None, Unset, list["YouTubeVideo"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                youtube_videos_type_0 = []
                _youtube_videos_type_0 = data
                for youtube_videos_type_0_item_data in _youtube_videos_type_0:
                    youtube_videos_type_0_item = YouTubeVideo.from_dict(youtube_videos_type_0_item_data)

                    youtube_videos_type_0.append(youtube_videos_type_0_item)

                return youtube_videos_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["YouTubeVideo"]], data)

        youtube_videos = _parse_youtube_videos(d.pop("youtubeVideos", UNSET))

        def _parse_reddit_posts(data: object) -> Union[None, Unset, list["RedditPost"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                reddit_posts_type_0 = []
                _reddit_posts_type_0 = data
                for reddit_posts_type_0_item_data in _reddit_posts_type_0:
                    reddit_posts_type_0_item = RedditPost.from_dict(reddit_posts_type_0_item_data)

                    reddit_posts_type_0.append(reddit_posts_type_0_item)

                return reddit_posts_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["RedditPost"]], data)

        reddit_posts = _parse_reddit_posts(d.pop("redditPosts", UNSET))

        coverage = cls(
            news_articles=news_articles,
            youtube_videos=youtube_videos,
            reddit_posts=reddit_posts,
        )

        coverage.additional_properties = d
        return coverage

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
