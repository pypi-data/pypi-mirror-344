from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.category_count import CategoryCount


T = TypeVar("T", bound="ChannelAverageValues")


@_attrs_define
class ChannelAverageValues:
    """
    Attributes:
        average_views (int):
        views_range (str):
        average_likes (int):
        likes_range (str):
        average_comments (int):
        comments_range (str):
        average_length (str):
        length_range (str):
        total_videos (int):
        category_counts (list['CategoryCount']):
        engagement (float):
    """

    average_views: int
    views_range: str
    average_likes: int
    likes_range: str
    average_comments: int
    comments_range: str
    average_length: str
    length_range: str
    total_videos: int
    category_counts: list["CategoryCount"]
    engagement: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        average_views = self.average_views

        views_range = self.views_range

        average_likes = self.average_likes

        likes_range = self.likes_range

        average_comments = self.average_comments

        comments_range = self.comments_range

        average_length = self.average_length

        length_range = self.length_range

        total_videos = self.total_videos

        category_counts = []
        for category_counts_item_data in self.category_counts:
            category_counts_item = category_counts_item_data.to_dict()
            category_counts.append(category_counts_item)

        engagement = self.engagement

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "averageViews": average_views,
                "viewsRange": views_range,
                "averageLikes": average_likes,
                "likesRange": likes_range,
                "averageComments": average_comments,
                "commentsRange": comments_range,
                "averageLength": average_length,
                "lengthRange": length_range,
                "totalVideos": total_videos,
                "categoryCounts": category_counts,
                "engagement": engagement,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_count import CategoryCount

        d = dict(src_dict)
        average_views = d.pop("averageViews")

        views_range = d.pop("viewsRange")

        average_likes = d.pop("averageLikes")

        likes_range = d.pop("likesRange")

        average_comments = d.pop("averageComments")

        comments_range = d.pop("commentsRange")

        average_length = d.pop("averageLength")

        length_range = d.pop("lengthRange")

        total_videos = d.pop("totalVideos")

        category_counts = []
        _category_counts = d.pop("categoryCounts")
        for category_counts_item_data in _category_counts:
            category_counts_item = CategoryCount.from_dict(category_counts_item_data)

            category_counts.append(category_counts_item)

        engagement = d.pop("engagement")

        channel_average_values = cls(
            average_views=average_views,
            views_range=views_range,
            average_likes=average_likes,
            likes_range=likes_range,
            average_comments=average_comments,
            comments_range=comments_range,
            average_length=average_length,
            length_range=length_range,
            total_videos=total_videos,
            category_counts=category_counts,
            engagement=engagement,
        )

        channel_average_values.additional_properties = d
        return channel_average_values

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
