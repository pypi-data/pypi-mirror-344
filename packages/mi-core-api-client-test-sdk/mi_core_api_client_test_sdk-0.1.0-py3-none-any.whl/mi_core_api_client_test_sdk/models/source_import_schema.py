from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_status import JobStatus
from ..models.source_types import SourceTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.articles_params_dto import ArticlesParamsDTO
    from ..models.articles_search_params_dto import ArticlesSearchParamsDTO
    from ..models.reddit_post_params_dto import RedditPostParamsDTO
    from ..models.reddit_search_params_dto import RedditSearchParamsDTO
    from ..models.reddit_user_params_dto import RedditUserParamsDTO
    from ..models.source_import_schema_source_metadata_type_0 import SourceImportSchemaSourceMetadataType0
    from ..models.source_import_schema_source_metadata_type_1_item import SourceImportSchemaSourceMetadataType1Item
    from ..models.sub_reddit_params_dto import SubRedditParamsDTO
    from ..models.youtube_channel_params_dto import YoutubeChannelParamsDTO
    from ..models.youtube_search_params_dto import YoutubeSearchParamsDTO
    from ..models.youtube_video_params_dto import YoutubeVideoParamsDTO


T = TypeVar("T", bound="SourceImportSchema")


@_attrs_define
class SourceImportSchema:
    """
    Attributes:
        source_type (SourceTypes): Enumeration class representing source types.
        params (Union['ArticlesParamsDTO', 'ArticlesSearchParamsDTO', 'RedditPostParamsDTO', 'RedditSearchParamsDTO',
            'RedditUserParamsDTO', 'SubRedditParamsDTO', 'YoutubeChannelParamsDTO', 'YoutubeSearchParamsDTO',
            'YoutubeVideoParamsDTO']):
        document_id (Union[None, UUID]):
        data_status (Union[JobStatus, None]):
        metadata_status (Union[JobStatus, None]):
        source_metadata (Union['SourceImportSchemaSourceMetadataType0',
            list['SourceImportSchemaSourceMetadataType1Item']]):
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
    document_id: Union[None, UUID]
    data_status: Union[JobStatus, None]
    metadata_status: Union[JobStatus, None]
    source_metadata: Union["SourceImportSchemaSourceMetadataType0", list["SourceImportSchemaSourceMetadataType1Item"]]
    input_query: Union[None, Unset, str] = UNSET
    input_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.articles_params_dto import ArticlesParamsDTO
        from ..models.reddit_post_params_dto import RedditPostParamsDTO
        from ..models.reddit_search_params_dto import RedditSearchParamsDTO
        from ..models.reddit_user_params_dto import RedditUserParamsDTO
        from ..models.source_import_schema_source_metadata_type_0 import SourceImportSchemaSourceMetadataType0
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

        document_id: Union[None, str]
        if isinstance(self.document_id, UUID):
            document_id = str(self.document_id)
        else:
            document_id = self.document_id

        data_status: Union[None, str]
        if isinstance(self.data_status, JobStatus):
            data_status = self.data_status.value
        else:
            data_status = self.data_status

        metadata_status: Union[None, str]
        if isinstance(self.metadata_status, JobStatus):
            metadata_status = self.metadata_status.value
        else:
            metadata_status = self.metadata_status

        source_metadata: Union[dict[str, Any], list[dict[str, Any]]]
        if isinstance(self.source_metadata, SourceImportSchemaSourceMetadataType0):
            source_metadata = self.source_metadata.to_dict()
        else:
            source_metadata = []
            for source_metadata_type_1_item_data in self.source_metadata:
                source_metadata_type_1_item = source_metadata_type_1_item_data.to_dict()
                source_metadata.append(source_metadata_type_1_item)

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
                "documentId": document_id,
                "dataStatus": data_status,
                "metadataStatus": metadata_status,
                "sourceMetadata": source_metadata,
            }
        )
        if input_query is not UNSET:
            field_dict["inputQuery"] = input_query
        if input_url is not UNSET:
            field_dict["inputUrl"] = input_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.articles_params_dto import ArticlesParamsDTO
        from ..models.articles_search_params_dto import ArticlesSearchParamsDTO
        from ..models.reddit_post_params_dto import RedditPostParamsDTO
        from ..models.reddit_search_params_dto import RedditSearchParamsDTO
        from ..models.reddit_user_params_dto import RedditUserParamsDTO
        from ..models.source_import_schema_source_metadata_type_0 import SourceImportSchemaSourceMetadataType0
        from ..models.source_import_schema_source_metadata_type_1_item import SourceImportSchemaSourceMetadataType1Item
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

        def _parse_data_status(data: object) -> Union[JobStatus, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_status_type_0 = JobStatus(data)

                return data_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[JobStatus, None], data)

        data_status = _parse_data_status(d.pop("dataStatus"))

        def _parse_metadata_status(data: object) -> Union[JobStatus, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                metadata_status_type_0 = JobStatus(data)

                return metadata_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[JobStatus, None], data)

        metadata_status = _parse_metadata_status(d.pop("metadataStatus"))

        def _parse_source_metadata(
            data: object,
        ) -> Union["SourceImportSchemaSourceMetadataType0", list["SourceImportSchemaSourceMetadataType1Item"]]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_metadata_type_0 = SourceImportSchemaSourceMetadataType0.from_dict(data)

                return source_metadata_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            source_metadata_type_1 = []
            _source_metadata_type_1 = data
            for source_metadata_type_1_item_data in _source_metadata_type_1:
                source_metadata_type_1_item = SourceImportSchemaSourceMetadataType1Item.from_dict(
                    source_metadata_type_1_item_data
                )

                source_metadata_type_1.append(source_metadata_type_1_item)

            return source_metadata_type_1

        source_metadata = _parse_source_metadata(d.pop("sourceMetadata"))

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

        source_import_schema = cls(
            source_type=source_type,
            params=params,
            document_id=document_id,
            data_status=data_status,
            metadata_status=metadata_status,
            source_metadata=source_metadata,
            input_query=input_query,
            input_url=input_url,
        )

        source_import_schema.additional_properties = d
        return source_import_schema

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
