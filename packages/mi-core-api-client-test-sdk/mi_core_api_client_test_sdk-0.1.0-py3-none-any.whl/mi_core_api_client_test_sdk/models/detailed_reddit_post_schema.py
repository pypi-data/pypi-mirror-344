import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.author_schema_dto import AuthorSchemaDTO
    from ..models.subreddit_schema_dto import SubredditSchemaDTO


T = TypeVar("T", bound="DetailedRedditPostSchema")


@_attrs_define
class DetailedRedditPostSchema:
    """
    Attributes:
        body (Union[None, str]):
        topic_id (UUID):
        url (str):
        title (str):
        published_date (datetime.date):
        author (AuthorSchemaDTO):
        subreddit (SubredditSchemaDTO):
        comments_count (int):
        upvotes (int):
        language (str):
        id (Union[Unset, UUID]):
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
        lock_status (Union[Unset, bool]):  Default: False.
    """

    body: Union[None, str]
    topic_id: UUID
    url: str
    title: str
    published_date: datetime.date
    author: "AuthorSchemaDTO"
    subreddit: "SubredditSchemaDTO"
    comments_count: int
    upvotes: int
    language: str
    id: Union[Unset, UUID] = UNSET
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    lock_status: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body: Union[None, str]
        body = self.body

        topic_id = str(self.topic_id)

        url = self.url

        title = self.title

        published_date = self.published_date.isoformat()

        author = self.author.to_dict()

        subreddit = self.subreddit.to_dict()

        comments_count = self.comments_count

        upvotes = self.upvotes

        language = self.language

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        lock_status = self.lock_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "topicId": topic_id,
                "url": url,
                "title": title,
                "publishedDate": published_date,
                "author": author,
                "subreddit": subreddit,
                "commentsCount": comments_count,
                "upvotes": upvotes,
                "language": language,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if lock_status is not UNSET:
            field_dict["lockStatus"] = lock_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.author_schema_dto import AuthorSchemaDTO
        from ..models.subreddit_schema_dto import SubredditSchemaDTO

        d = dict(src_dict)

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

        topic_id = UUID(d.pop("topicId"))

        url = d.pop("url")

        title = d.pop("title")

        published_date = isoparse(d.pop("publishedDate")).date()

        author = AuthorSchemaDTO.from_dict(d.pop("author"))

        subreddit = SubredditSchemaDTO.from_dict(d.pop("subreddit"))

        comments_count = d.pop("commentsCount")

        upvotes = d.pop("upvotes")

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

        lock_status = d.pop("lockStatus", UNSET)

        detailed_reddit_post_schema = cls(
            body=body,
            topic_id=topic_id,
            url=url,
            title=title,
            published_date=published_date,
            author=author,
            subreddit=subreddit,
            comments_count=comments_count,
            upvotes=upvotes,
            language=language,
            id=id,
            updated_at=updated_at,
            lock_status=lock_status,
        )

        detailed_reddit_post_schema.additional_properties = d
        return detailed_reddit_post_schema

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
