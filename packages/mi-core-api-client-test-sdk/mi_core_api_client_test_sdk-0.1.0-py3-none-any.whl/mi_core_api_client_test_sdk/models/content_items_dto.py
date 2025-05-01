import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.source_types import SourceTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_metadata_dto import ArticleMetadataDTO
    from ..models.content_item_source import ContentItemSource
    from ..models.custom_column_value_dto import CustomColumnValueDTO
    from ..models.reddit_post_metadata_dto import RedditPostMetadataDTO
    from ..models.you_tube_video_metadata_dto import YouTubeVideoMetadataDTO


T = TypeVar("T", bound="ContentItemsDTO")


@_attrs_define
class ContentItemsDTO:
    """
    Attributes:
        name (str):
        description (str):
        source_type (SourceTypes): Enumeration class representing source types.
        created_at (datetime.datetime):
        metadata (Union['ArticleMetadataDTO', 'RedditPostMetadataDTO', 'YouTubeVideoMetadataDTO']):
        link (Union[None, Unset, str]):
        document_id (Union[None, UUID, Unset]):
        sources (Union[Unset, list['ContentItemSource']]):
        custom_fields (Union[Unset, list['CustomColumnValueDTO']]):
    """

    name: str
    description: str
    source_type: SourceTypes
    created_at: datetime.datetime
    metadata: Union["ArticleMetadataDTO", "RedditPostMetadataDTO", "YouTubeVideoMetadataDTO"]
    link: Union[None, Unset, str] = UNSET
    document_id: Union[None, UUID, Unset] = UNSET
    sources: Union[Unset, list["ContentItemSource"]] = UNSET
    custom_fields: Union[Unset, list["CustomColumnValueDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.reddit_post_metadata_dto import RedditPostMetadataDTO
        from ..models.you_tube_video_metadata_dto import YouTubeVideoMetadataDTO

        name = self.name

        description = self.description

        source_type = self.source_type.value

        created_at = self.created_at.isoformat()

        metadata: dict[str, Any]
        if isinstance(self.metadata, YouTubeVideoMetadataDTO):
            metadata = self.metadata.to_dict()
        elif isinstance(self.metadata, RedditPostMetadataDTO):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata.to_dict()

        link: Union[None, Unset, str]
        if isinstance(self.link, Unset):
            link = UNSET
        else:
            link = self.link

        document_id: Union[None, Unset, str]
        if isinstance(self.document_id, Unset):
            document_id = UNSET
        elif isinstance(self.document_id, UUID):
            document_id = str(self.document_id)
        else:
            document_id = self.document_id

        sources: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sources, Unset):
            sources = []
            for sources_item_data in self.sources:
                sources_item = sources_item_data.to_dict()
                sources.append(sources_item)

        custom_fields: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = []
            for custom_fields_item_data in self.custom_fields:
                custom_fields_item = custom_fields_item_data.to_dict()
                custom_fields.append(custom_fields_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "sourceType": source_type,
                "createdAt": created_at,
                "metadata": metadata,
            }
        )
        if link is not UNSET:
            field_dict["link"] = link
        if document_id is not UNSET:
            field_dict["documentId"] = document_id
        if sources is not UNSET:
            field_dict["sources"] = sources
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_metadata_dto import ArticleMetadataDTO
        from ..models.content_item_source import ContentItemSource
        from ..models.custom_column_value_dto import CustomColumnValueDTO
        from ..models.reddit_post_metadata_dto import RedditPostMetadataDTO
        from ..models.you_tube_video_metadata_dto import YouTubeVideoMetadataDTO

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        source_type = SourceTypes(d.pop("sourceType"))

        created_at = isoparse(d.pop("createdAt"))

        def _parse_metadata(
            data: object,
        ) -> Union["ArticleMetadataDTO", "RedditPostMetadataDTO", "YouTubeVideoMetadataDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = YouTubeVideoMetadataDTO.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_1 = RedditPostMetadataDTO.from_dict(data)

                return metadata_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            metadata_type_2 = ArticleMetadataDTO.from_dict(data)

            return metadata_type_2

        metadata = _parse_metadata(d.pop("metadata"))

        def _parse_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        link = _parse_link(d.pop("link", UNSET))

        def _parse_document_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                document_id_type_0 = UUID(data)

                return document_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        document_id = _parse_document_id(d.pop("documentId", UNSET))

        sources = []
        _sources = d.pop("sources", UNSET)
        for sources_item_data in _sources or []:
            sources_item = ContentItemSource.from_dict(sources_item_data)

            sources.append(sources_item)

        custom_fields = []
        _custom_fields = d.pop("customFields", UNSET)
        for custom_fields_item_data in _custom_fields or []:
            custom_fields_item = CustomColumnValueDTO.from_dict(custom_fields_item_data)

            custom_fields.append(custom_fields_item)

        content_items_dto = cls(
            name=name,
            description=description,
            source_type=source_type,
            created_at=created_at,
            metadata=metadata,
            link=link,
            document_id=document_id,
            sources=sources,
            custom_fields=custom_fields,
        )

        content_items_dto.additional_properties = d
        return content_items_dto

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
