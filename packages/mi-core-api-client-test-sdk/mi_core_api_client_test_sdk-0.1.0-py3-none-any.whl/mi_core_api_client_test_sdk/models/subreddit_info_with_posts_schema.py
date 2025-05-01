import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.reddit_post_schema_document import RedditPostSchemaDocument


T = TypeVar("T", bound="SubredditInfoWithPostsSchema")


@_attrs_define
class SubredditInfoWithPostsSchema:
    """
    Attributes:
        body (Union[None, str]):
        topic_id (UUID):
        url (str):
        title (str):
        members (int):
        online_members (int):
        thumbnail_url (str):
        rank (Union[None, str]):
        language (str):
        id (Union[Unset, UUID]):
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
        posts_comments_count (Union[Unset, int]):  Default: 0.
        posts_upvotes (Union[Unset, int]):  Default: 0.
        posts_count (Union[Unset, int]):  Default: 0.
        posts (Union[Unset, list['RedditPostSchemaDocument']]):
    """

    body: Union[None, str]
    topic_id: UUID
    url: str
    title: str
    members: int
    online_members: int
    thumbnail_url: str
    rank: Union[None, str]
    language: str
    id: Union[Unset, UUID] = UNSET
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    posts_comments_count: Union[Unset, int] = 0
    posts_upvotes: Union[Unset, int] = 0
    posts_count: Union[Unset, int] = 0
    posts: Union[Unset, list["RedditPostSchemaDocument"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body: Union[None, str]
        body = self.body

        topic_id = str(self.topic_id)

        url = self.url

        title = self.title

        members = self.members

        online_members = self.online_members

        thumbnail_url = self.thumbnail_url

        rank: Union[None, str]
        rank = self.rank

        language = self.language

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        posts_comments_count = self.posts_comments_count

        posts_upvotes = self.posts_upvotes

        posts_count = self.posts_count

        posts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.posts, Unset):
            posts = []
            for posts_item_data in self.posts:
                posts_item = posts_item_data.to_dict()
                posts.append(posts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "topicId": topic_id,
                "url": url,
                "title": title,
                "members": members,
                "onlineMembers": online_members,
                "thumbnailUrl": thumbnail_url,
                "rank": rank,
                "language": language,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if posts_comments_count is not UNSET:
            field_dict["postsCommentsCount"] = posts_comments_count
        if posts_upvotes is not UNSET:
            field_dict["postsUpvotes"] = posts_upvotes
        if posts_count is not UNSET:
            field_dict["postsCount"] = posts_count
        if posts is not UNSET:
            field_dict["posts"] = posts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.reddit_post_schema_document import RedditPostSchemaDocument

        d = dict(src_dict)

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

        topic_id = UUID(d.pop("topicId"))

        url = d.pop("url")

        title = d.pop("title")

        members = d.pop("members")

        online_members = d.pop("onlineMembers")

        thumbnail_url = d.pop("thumbnailUrl")

        def _parse_rank(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        rank = _parse_rank(d.pop("rank"))

        language = d.pop("language")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        posts_comments_count = d.pop("postsCommentsCount", UNSET)

        posts_upvotes = d.pop("postsUpvotes", UNSET)

        posts_count = d.pop("postsCount", UNSET)

        posts = []
        _posts = d.pop("posts", UNSET)
        for posts_item_data in _posts or []:
            posts_item = RedditPostSchemaDocument.from_dict(posts_item_data)

            posts.append(posts_item)

        subreddit_info_with_posts_schema = cls(
            body=body,
            topic_id=topic_id,
            url=url,
            title=title,
            members=members,
            online_members=online_members,
            thumbnail_url=thumbnail_url,
            rank=rank,
            language=language,
            id=id,
            updated_at=updated_at,
            posts_comments_count=posts_comments_count,
            posts_upvotes=posts_upvotes,
            posts_count=posts_count,
            posts=posts,
        )

        subreddit_info_with_posts_schema.additional_properties = d
        return subreddit_info_with_posts_schema

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
