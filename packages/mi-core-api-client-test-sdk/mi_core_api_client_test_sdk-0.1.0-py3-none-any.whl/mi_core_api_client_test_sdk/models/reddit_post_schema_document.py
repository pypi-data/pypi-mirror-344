import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RedditPostSchemaDocument")


@_attrs_define
class RedditPostSchemaDocument:
    """
    Attributes:
        body (Union[None, str]):
        topic_id (UUID):
        url (str):
        title (str):
        subreddit_id (UUID):
        published_date (datetime.date):
        comments_count (int):
        upvotes (int):
        language (str):
        id (Union[Unset, UUID]):
        updated_at (Union[Unset, datetime.datetime]):  Default: isoparse('2025-05-01T06:12:12.440922Z').
        author_id (Union[None, UUID, Unset]):
        lock_status (Union[Unset, bool]):  Default: False.
        subreddit_name (Union[None, Unset, str]):
        author_name (Union[None, Unset, str]):
    """

    body: Union[None, str]
    topic_id: UUID
    url: str
    title: str
    subreddit_id: UUID
    published_date: datetime.date
    comments_count: int
    upvotes: int
    language: str
    id: Union[Unset, UUID] = UNSET
    updated_at: Union[Unset, datetime.datetime] = isoparse("2025-05-01T06:12:12.440922Z")
    author_id: Union[None, UUID, Unset] = UNSET
    lock_status: Union[Unset, bool] = False
    subreddit_name: Union[None, Unset, str] = UNSET
    author_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body: Union[None, str]
        body = self.body

        topic_id = str(self.topic_id)

        url = self.url

        title = self.title

        subreddit_id = str(self.subreddit_id)

        published_date = self.published_date.isoformat()

        comments_count = self.comments_count

        upvotes = self.upvotes

        language = self.language

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        author_id: Union[None, Unset, str]
        if isinstance(self.author_id, Unset):
            author_id = UNSET
        elif isinstance(self.author_id, UUID):
            author_id = str(self.author_id)
        else:
            author_id = self.author_id

        lock_status = self.lock_status

        subreddit_name: Union[None, Unset, str]
        if isinstance(self.subreddit_name, Unset):
            subreddit_name = UNSET
        else:
            subreddit_name = self.subreddit_name

        author_name: Union[None, Unset, str]
        if isinstance(self.author_name, Unset):
            author_name = UNSET
        else:
            author_name = self.author_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "topicId": topic_id,
                "url": url,
                "title": title,
                "subredditId": subreddit_id,
                "publishedDate": published_date,
                "commentsCount": comments_count,
                "upvotes": upvotes,
                "language": language,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if author_id is not UNSET:
            field_dict["authorId"] = author_id
        if lock_status is not UNSET:
            field_dict["lockStatus"] = lock_status
        if subreddit_name is not UNSET:
            field_dict["subredditName"] = subreddit_name
        if author_name is not UNSET:
            field_dict["authorName"] = author_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_body(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        body = _parse_body(d.pop("body"))

        topic_id = UUID(d.pop("topicId"))

        url = d.pop("url")

        title = d.pop("title")

        subreddit_id = UUID(d.pop("subredditId"))

        published_date = isoparse(d.pop("publishedDate")).date()

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

        def _parse_author_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                author_id_type_0 = UUID(data)

                return author_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        author_id = _parse_author_id(d.pop("authorId", UNSET))

        lock_status = d.pop("lockStatus", UNSET)

        def _parse_subreddit_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subreddit_name = _parse_subreddit_name(d.pop("subredditName", UNSET))

        def _parse_author_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        author_name = _parse_author_name(d.pop("authorName", UNSET))

        reddit_post_schema_document = cls(
            body=body,
            topic_id=topic_id,
            url=url,
            title=title,
            subreddit_id=subreddit_id,
            published_date=published_date,
            comments_count=comments_count,
            upvotes=upvotes,
            language=language,
            id=id,
            updated_at=updated_at,
            author_id=author_id,
            lock_status=lock_status,
            subreddit_name=subreddit_name,
            author_name=author_name,
        )

        reddit_post_schema_document.additional_properties = d
        return reddit_post_schema_document

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
