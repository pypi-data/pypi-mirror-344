import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status import JobStatus
from ..models.source_types import SourceTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.articles_params_dto import ArticlesParamsDTO
    from ..models.articles_search_params_dto import ArticlesSearchParamsDTO
    from ..models.collection_info import CollectionInfo
    from ..models.reddit_post_params_dto import RedditPostParamsDTO
    from ..models.reddit_search_params_dto import RedditSearchParamsDTO
    from ..models.reddit_user_params_dto import RedditUserParamsDTO
    from ..models.source_get_schema_source_metadata_type_0 import SourceGetSchemaSourceMetadataType0
    from ..models.source_get_schema_source_metadata_type_1_item import SourceGetSchemaSourceMetadataType1Item
    from ..models.sub_reddit_params_dto import SubRedditParamsDTO
    from ..models.youtube_channel_params_dto import YoutubeChannelParamsDTO
    from ..models.youtube_search_params_dto import YoutubeSearchParamsDTO
    from ..models.youtube_video_params_dto import YoutubeVideoParamsDTO


T = TypeVar("T", bound="SourceGetSchema")


@_attrs_define
class SourceGetSchema:
    """
    Attributes:
        source_type (SourceTypes): Enumeration class representing source types.
        params (Union['ArticlesParamsDTO', 'ArticlesSearchParamsDTO', 'RedditPostParamsDTO', 'RedditSearchParamsDTO',
            'RedditUserParamsDTO', 'SubRedditParamsDTO', 'YoutubeChannelParamsDTO', 'YoutubeSearchParamsDTO',
            'YoutubeVideoParamsDTO']):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        document_id (Union[None, UUID]):
        data_status (JobStatus): Enumeration class representing job statuses.

            Attributes:
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
        metadata_status (JobStatus): Enumeration class representing job statuses.

            Attributes:
                CREATED: Represents created job status.
                PROCESSING: Represents processing job status.
                COMPLETED: Represents completed job status.
                FAILED: Represents failed job status.
        collections (list['CollectionInfo']):
        id (Union[Unset, UUID]):
        source_metadata (Union['SourceGetSchemaSourceMetadataType0', None, Unset,
            list['SourceGetSchemaSourceMetadataType1Item']]):
        input_query (Union[None, Unset, str]):
        input_url (Union[None, Unset, str]):
    """

    source_type: SourceTypes
    params: Union[
        "ArticlesParamsDTO",
        "ArticlesSearchParamsDTO",
        "RedditPostParamsDTO",
        "RedditSearchParamsDTO",
        "RedditUserParamsDTO",
        "SubRedditParamsDTO",
        "YoutubeChannelParamsDTO",
        "YoutubeSearchParamsDTO",
        "YoutubeVideoParamsDTO",
    ]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    document_id: Union[None, UUID]
    data_status: JobStatus
    metadata_status: JobStatus
    collections: list["CollectionInfo"]
    id: Union[Unset, UUID] = UNSET
    source_metadata: Union[
        "SourceGetSchemaSourceMetadataType0", None, Unset, list["SourceGetSchemaSourceMetadataType1Item"]
    ] = UNSET
    input_query: Union[None, Unset, str] = UNSET
    input_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.articles_params_dto import ArticlesParamsDTO
        from ..models.reddit_post_params_dto import RedditPostParamsDTO
        from ..models.reddit_search_params_dto import RedditSearchParamsDTO
        from ..models.reddit_user_params_dto import RedditUserParamsDTO
        from ..models.source_get_schema_source_metadata_type_0 import SourceGetSchemaSourceMetadataType0
        from ..models.sub_reddit_params_dto import SubRedditParamsDTO
        from ..models.youtube_channel_params_dto import YoutubeChannelParamsDTO
        from ..models.youtube_search_params_dto import YoutubeSearchParamsDTO
        from ..models.youtube_video_params_dto import YoutubeVideoParamsDTO

        source_type = self.source_type.value

        params: dict[str, Any]
        if isinstance(self.params, YoutubeChannelParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, YoutubeSearchParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, YoutubeVideoParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, SubRedditParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, RedditUserParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, RedditSearchParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, RedditPostParamsDTO):
            params = self.params.to_dict()
        elif isinstance(self.params, ArticlesParamsDTO):
            params = self.params.to_dict()
        else:
            params = self.params.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        document_id: Union[None, str]
        if isinstance(self.document_id, UUID):
            document_id = str(self.document_id)
        else:
            document_id = self.document_id

        data_status = self.data_status.value

        metadata_status = self.metadata_status.value

        collections = []
        for collections_item_data in self.collections:
            collections_item = collections_item_data.to_dict()
            collections.append(collections_item)

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        source_metadata: Union[None, Unset, dict[str, Any], list[dict[str, Any]]]
        if isinstance(self.source_metadata, Unset):
            source_metadata = UNSET
        elif isinstance(self.source_metadata, SourceGetSchemaSourceMetadataType0):
            source_metadata = self.source_metadata.to_dict()
        elif isinstance(self.source_metadata, list):
            source_metadata = []
            for source_metadata_type_1_item_data in self.source_metadata:
                source_metadata_type_1_item = source_metadata_type_1_item_data.to_dict()
                source_metadata.append(source_metadata_type_1_item)

        else:
            source_metadata = self.source_metadata

        input_query: Union[None, Unset, str]
        if isinstance(self.input_query, Unset):
            input_query = UNSET
        else:
            input_query = self.input_query

        input_url: Union[None, Unset, str]
        if isinstance(self.input_url, Unset):
            input_url = UNSET
        else:
            input_url = self.input_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sourceType": source_type,
                "params": params,
                "createdAt": created_at,
                "updatedAt": updated_at,
                "documentId": document_id,
                "dataStatus": data_status,
                "metadataStatus": metadata_status,
                "collections": collections,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if source_metadata is not UNSET:
            field_dict["sourceMetadata"] = source_metadata
        if input_query is not UNSET:
            field_dict["inputQuery"] = input_query
        if input_url is not UNSET:
            field_dict["inputUrl"] = input_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.articles_params_dto import ArticlesParamsDTO
        from ..models.articles_search_params_dto import ArticlesSearchParamsDTO
        from ..models.collection_info import CollectionInfo
        from ..models.reddit_post_params_dto import RedditPostParamsDTO
        from ..models.reddit_search_params_dto import RedditSearchParamsDTO
        from ..models.reddit_user_params_dto import RedditUserParamsDTO
        from ..models.source_get_schema_source_metadata_type_0 import SourceGetSchemaSourceMetadataType0
        from ..models.source_get_schema_source_metadata_type_1_item import SourceGetSchemaSourceMetadataType1Item
        from ..models.sub_reddit_params_dto import SubRedditParamsDTO
        from ..models.youtube_channel_params_dto import YoutubeChannelParamsDTO
        from ..models.youtube_search_params_dto import YoutubeSearchParamsDTO
        from ..models.youtube_video_params_dto import YoutubeVideoParamsDTO

        d = dict(src_dict)
        source_type = SourceTypes(d.pop("sourceType"))

        def _parse_params(
            data: object,
        ) -> Union[
            "ArticlesParamsDTO",
            "ArticlesSearchParamsDTO",
            "RedditPostParamsDTO",
            "RedditSearchParamsDTO",
            "RedditUserParamsDTO",
            "SubRedditParamsDTO",
            "YoutubeChannelParamsDTO",
            "YoutubeSearchParamsDTO",
            "YoutubeVideoParamsDTO",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_0 = YoutubeChannelParamsDTO.from_dict(data)

                return params_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_1 = YoutubeSearchParamsDTO.from_dict(data)

                return params_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_2 = YoutubeVideoParamsDTO.from_dict(data)

                return params_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_3 = SubRedditParamsDTO.from_dict(data)

                return params_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_4 = RedditUserParamsDTO.from_dict(data)

                return params_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_5 = RedditSearchParamsDTO.from_dict(data)

                return params_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_6 = RedditPostParamsDTO.from_dict(data)

                return params_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                params_type_7 = ArticlesParamsDTO.from_dict(data)

                return params_type_7
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            params_type_8 = ArticlesSearchParamsDTO.from_dict(data)

            return params_type_8

        params = _parse_params(d.pop("params"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        def _parse_document_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                document_id_type_0 = UUID(data)

                return document_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        document_id = _parse_document_id(d.pop("documentId"))

        data_status = JobStatus(d.pop("dataStatus"))

        metadata_status = JobStatus(d.pop("metadataStatus"))

        collections = []
        _collections = d.pop("collections")
        for collections_item_data in _collections:
            collections_item = CollectionInfo.from_dict(collections_item_data)

            collections.append(collections_item)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        def _parse_source_metadata(
            data: object,
        ) -> Union["SourceGetSchemaSourceMetadataType0", None, Unset, list["SourceGetSchemaSourceMetadataType1Item"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_metadata_type_0 = SourceGetSchemaSourceMetadataType0.from_dict(data)

                return source_metadata_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                source_metadata_type_1 = []
                _source_metadata_type_1 = data
                for source_metadata_type_1_item_data in _source_metadata_type_1:
                    source_metadata_type_1_item = SourceGetSchemaSourceMetadataType1Item.from_dict(
                        source_metadata_type_1_item_data
                    )

                    source_metadata_type_1.append(source_metadata_type_1_item)

                return source_metadata_type_1
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "SourceGetSchemaSourceMetadataType0", None, Unset, list["SourceGetSchemaSourceMetadataType1Item"]
                ],
                data,
            )

        source_metadata = _parse_source_metadata(d.pop("sourceMetadata", UNSET))

        def _parse_input_query(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_query = _parse_input_query(d.pop("inputQuery", UNSET))

        def _parse_input_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_url = _parse_input_url(d.pop("inputUrl", UNSET))

        source_get_schema = cls(
            source_type=source_type,
            params=params,
            created_at=created_at,
            updated_at=updated_at,
            document_id=document_id,
            data_status=data_status,
            metadata_status=metadata_status,
            collections=collections,
            id=id,
            source_metadata=source_metadata,
            input_query=input_query,
            input_url=input_url,
        )

        source_get_schema.additional_properties = d
        return source_get_schema

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
