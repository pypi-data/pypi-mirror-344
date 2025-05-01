import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.report_type import ReportType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportWithRunningCollectionSchema")


@_attrs_define
class ReportWithRunningCollectionSchema:
    """
    Attributes:
        name (str):
        type_ (ReportType): Enumeration class representing report types.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        description (Union[None, Unset, str]):
        query (Union[None, Unset, str]):
        prompt (Union[None, Unset, str]):
        llm_model (Union[None, Unset, str]):
        id (Union[Unset, UUID]):
        summary (Union[None, Unset, str]):
        summary_youtube (Union[None, Unset, str]):
        summary_reddit (Union[None, Unset, str]):
        summary_articles (Union[None, Unset, str]):
        running_collection_id (Union[None, UUID, Unset]):
    """

    name: str
    type_: ReportType
    created_at: datetime.datetime
    updated_at: datetime.datetime
    description: Union[None, Unset, str] = UNSET
    query: Union[None, Unset, str] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    llm_model: Union[None, Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    summary: Union[None, Unset, str] = UNSET
    summary_youtube: Union[None, Unset, str] = UNSET
    summary_reddit: Union[None, Unset, str] = UNSET
    summary_articles: Union[None, Unset, str] = UNSET
    running_collection_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        query: Union[None, Unset, str]
        if isinstance(self.query, Unset):
            query = UNSET
        else:
            query = self.query

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        llm_model: Union[None, Unset, str]
        if isinstance(self.llm_model, Unset):
            llm_model = UNSET
        else:
            llm_model = self.llm_model

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        summary: Union[None, Unset, str]
        if isinstance(self.summary, Unset):
            summary = UNSET
        else:
            summary = self.summary

        summary_youtube: Union[None, Unset, str]
        if isinstance(self.summary_youtube, Unset):
            summary_youtube = UNSET
        else:
            summary_youtube = self.summary_youtube

        summary_reddit: Union[None, Unset, str]
        if isinstance(self.summary_reddit, Unset):
            summary_reddit = UNSET
        else:
            summary_reddit = self.summary_reddit

        summary_articles: Union[None, Unset, str]
        if isinstance(self.summary_articles, Unset):
            summary_articles = UNSET
        else:
            summary_articles = self.summary_articles

        running_collection_id: Union[None, Unset, str]
        if isinstance(self.running_collection_id, Unset):
            running_collection_id = UNSET
        elif isinstance(self.running_collection_id, UUID):
            running_collection_id = str(self.running_collection_id)
        else:
            running_collection_id = self.running_collection_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if query is not UNSET:
            field_dict["query"] = query
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if llm_model is not UNSET:
            field_dict["llmModel"] = llm_model
        if id is not UNSET:
            field_dict["id"] = id
        if summary is not UNSET:
            field_dict["summary"] = summary
        if summary_youtube is not UNSET:
            field_dict["summaryYoutube"] = summary_youtube
        if summary_reddit is not UNSET:
            field_dict["summaryReddit"] = summary_reddit
        if summary_articles is not UNSET:
            field_dict["summaryArticles"] = summary_articles
        if running_collection_id is not UNSET:
            field_dict["runningCollectionId"] = running_collection_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = ReportType(d.pop("type"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_query(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        query = _parse_query(d.pop("query", UNSET))

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_llm_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        llm_model = _parse_llm_model(d.pop("llmModel", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        def _parse_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary = _parse_summary(d.pop("summary", UNSET))

        def _parse_summary_youtube(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary_youtube = _parse_summary_youtube(d.pop("summaryYoutube", UNSET))

        def _parse_summary_reddit(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary_reddit = _parse_summary_reddit(d.pop("summaryReddit", UNSET))

        def _parse_summary_articles(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        summary_articles = _parse_summary_articles(d.pop("summaryArticles", UNSET))

        def _parse_running_collection_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                running_collection_id_type_0 = UUID(data)

                return running_collection_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        running_collection_id = _parse_running_collection_id(d.pop("runningCollectionId", UNSET))

        report_with_running_collection_schema = cls(
            name=name,
            type_=type_,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
            query=query,
            prompt=prompt,
            llm_model=llm_model,
            id=id,
            summary=summary,
            summary_youtube=summary_youtube,
            summary_reddit=summary_reddit,
            summary_articles=summary_articles,
            running_collection_id=running_collection_id,
        )

        report_with_running_collection_schema.additional_properties = d
        return report_with_running_collection_schema

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
