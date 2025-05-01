from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DocumentCountInfo")


@_attrs_define
class DocumentCountInfo:
    """
    Attributes:
        youtube_channel_info (Union[Unset, int]):  Default: 0.
        youtube_video (Union[Unset, int]):  Default: 0.
        youtube_comment (Union[Unset, int]):  Default: 0.
        subreddit_info (Union[Unset, int]):  Default: 0.
        reddit_post (Union[Unset, int]):  Default: 0.
        reddit_comment (Union[Unset, int]):  Default: 0.
        news_article (Union[Unset, int]):  Default: 0.
    """

    youtube_channel_info: Union[Unset, int] = 0
    youtube_video: Union[Unset, int] = 0
    youtube_comment: Union[Unset, int] = 0
    subreddit_info: Union[Unset, int] = 0
    reddit_post: Union[Unset, int] = 0
    reddit_comment: Union[Unset, int] = 0
    news_article: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_channel_info = self.youtube_channel_info

        youtube_video = self.youtube_video

        youtube_comment = self.youtube_comment

        subreddit_info = self.subreddit_info

        reddit_post = self.reddit_post

        reddit_comment = self.reddit_comment

        news_article = self.news_article

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if youtube_channel_info is not UNSET:
            field_dict["youtubeChannelInfo"] = youtube_channel_info
        if youtube_video is not UNSET:
            field_dict["youtubeVideo"] = youtube_video
        if youtube_comment is not UNSET:
            field_dict["youtubeComment"] = youtube_comment
        if subreddit_info is not UNSET:
            field_dict["subredditInfo"] = subreddit_info
        if reddit_post is not UNSET:
            field_dict["redditPost"] = reddit_post
        if reddit_comment is not UNSET:
            field_dict["redditComment"] = reddit_comment
        if news_article is not UNSET:
            field_dict["newsArticle"] = news_article

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        youtube_channel_info = d.pop("youtubeChannelInfo", UNSET)

        youtube_video = d.pop("youtubeVideo", UNSET)

        youtube_comment = d.pop("youtubeComment", UNSET)

        subreddit_info = d.pop("subredditInfo", UNSET)

        reddit_post = d.pop("redditPost", UNSET)

        reddit_comment = d.pop("redditComment", UNSET)

        news_article = d.pop("newsArticle", UNSET)

        document_count_info = cls(
            youtube_channel_info=youtube_channel_info,
            youtube_video=youtube_video,
            youtube_comment=youtube_comment,
            subreddit_info=subreddit_info,
            reddit_post=reddit_post,
            reddit_comment=reddit_comment,
            news_article=news_article,
        )

        document_count_info.additional_properties = d
        return document_count_info

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
