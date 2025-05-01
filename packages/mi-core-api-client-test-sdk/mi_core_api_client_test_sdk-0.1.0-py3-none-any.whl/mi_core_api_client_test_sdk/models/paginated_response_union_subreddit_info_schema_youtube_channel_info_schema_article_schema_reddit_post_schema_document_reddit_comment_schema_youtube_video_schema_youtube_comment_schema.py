from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_schema import ArticleSchema
    from ..models.reddit_comment_schema import RedditCommentSchema
    from ..models.reddit_post_schema_document import RedditPostSchemaDocument
    from ..models.subreddit_info_schema import SubredditInfoSchema
    from ..models.youtube_channel_info_schema import YoutubeChannelInfoSchema
    from ..models.youtube_comment_schema import YoutubeCommentSchema
    from ..models.youtube_video_schema import YoutubeVideoSchema


T = TypeVar(
    "T",
    bound="PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema",
)


@_attrs_define
class PaginatedResponseUnionSubredditInfoSchemaYoutubeChannelInfoSchemaArticleSchemaRedditPostSchemaDocumentRedditCommentSchemaYoutubeVideoSchemaYoutubeCommentSchema:
    """
    Attributes:
        count (int): Number of total items
        total_pages (int): Number of total pages
        input_items (Union[Unset, list[Union['ArticleSchema', 'RedditCommentSchema', 'RedditPostSchemaDocument',
            'SubredditInfoSchema', 'YoutubeChannelInfoSchema', 'YoutubeCommentSchema', 'YoutubeVideoSchema']]]): List of
            items before pagination
    """

    count: int
    total_pages: int
    input_items: Union[
        Unset,
        list[
            Union[
                "ArticleSchema",
                "RedditCommentSchema",
                "RedditPostSchemaDocument",
                "SubredditInfoSchema",
                "YoutubeChannelInfoSchema",
                "YoutubeCommentSchema",
                "YoutubeVideoSchema",
            ]
        ],
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.article_schema import ArticleSchema
        from ..models.reddit_comment_schema import RedditCommentSchema
        from ..models.reddit_post_schema_document import RedditPostSchemaDocument
        from ..models.subreddit_info_schema import SubredditInfoSchema
        from ..models.youtube_channel_info_schema import YoutubeChannelInfoSchema
        from ..models.youtube_video_schema import YoutubeVideoSchema

        count = self.count

        total_pages = self.total_pages

        input_items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.input_items, Unset):
            input_items = []
            for input_items_item_data in self.input_items:
                input_items_item: dict[str, Any]
                if isinstance(input_items_item_data, SubredditInfoSchema):
                    input_items_item = input_items_item_data.to_dict()
                elif isinstance(input_items_item_data, YoutubeChannelInfoSchema):
                    input_items_item = input_items_item_data.to_dict()
                elif isinstance(input_items_item_data, ArticleSchema):
                    input_items_item = input_items_item_data.to_dict()
                elif isinstance(input_items_item_data, RedditPostSchemaDocument):
                    input_items_item = input_items_item_data.to_dict()
                elif isinstance(input_items_item_data, RedditCommentSchema):
                    input_items_item = input_items_item_data.to_dict()
                elif isinstance(input_items_item_data, YoutubeVideoSchema):
                    input_items_item = input_items_item_data.to_dict()
                else:
                    input_items_item = input_items_item_data.to_dict()

                input_items.append(input_items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "totalPages": total_pages,
            }
        )
        if input_items is not UNSET:
            field_dict["inputItems"] = input_items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_schema import ArticleSchema
        from ..models.reddit_comment_schema import RedditCommentSchema
        from ..models.reddit_post_schema_document import RedditPostSchemaDocument
        from ..models.subreddit_info_schema import SubredditInfoSchema
        from ..models.youtube_channel_info_schema import YoutubeChannelInfoSchema
        from ..models.youtube_comment_schema import YoutubeCommentSchema
        from ..models.youtube_video_schema import YoutubeVideoSchema

        d = dict(src_dict)
        count = d.pop("count")

        total_pages = d.pop("totalPages")

        input_items = []
        _input_items = d.pop("inputItems", UNSET)
        for input_items_item_data in _input_items or []:

            def _parse_input_items_item(
                data: object,
            ) -> Union[
                "ArticleSchema",
                "RedditCommentSchema",
                "RedditPostSchemaDocument",
                "SubredditInfoSchema",
                "YoutubeChannelInfoSchema",
                "YoutubeCommentSchema",
                "YoutubeVideoSchema",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    input_items_item_type_0 = SubredditInfoSchema.from_dict(data)

                    return input_items_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    input_items_item_type_1 = YoutubeChannelInfoSchema.from_dict(data)

                    return input_items_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    input_items_item_type_2 = ArticleSchema.from_dict(data)

                    return input_items_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    input_items_item_type_3 = RedditPostSchemaDocument.from_dict(data)

                    return input_items_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    input_items_item_type_4 = RedditCommentSchema.from_dict(data)

                    return input_items_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    input_items_item_type_5 = YoutubeVideoSchema.from_dict(data)

                    return input_items_item_type_5
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                input_items_item_type_6 = YoutubeCommentSchema.from_dict(data)

                return input_items_item_type_6

            input_items_item = _parse_input_items_item(input_items_item_data)

            input_items.append(input_items_item)

        paginated_response_union_subreddit_info_schema_youtube_channel_info_schema_article_schema_reddit_post_schema_document_reddit_comment_schema_youtube_video_schema_youtube_comment_schema = cls(
            count=count,
            total_pages=total_pages,
            input_items=input_items,
        )

        paginated_response_union_subreddit_info_schema_youtube_channel_info_schema_article_schema_reddit_post_schema_document_reddit_comment_schema_youtube_video_schema_youtube_comment_schema.additional_properties = d
        return paginated_response_union_subreddit_info_schema_youtube_channel_info_schema_article_schema_reddit_post_schema_document_reddit_comment_schema_youtube_video_schema_youtube_comment_schema

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
