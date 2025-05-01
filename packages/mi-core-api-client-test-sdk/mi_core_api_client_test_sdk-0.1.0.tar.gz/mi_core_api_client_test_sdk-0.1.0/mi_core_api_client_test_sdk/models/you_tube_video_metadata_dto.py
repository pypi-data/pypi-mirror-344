from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.parent_item import ParentItem


T = TypeVar("T", bound="YouTubeVideoMetadataDTO")


@_attrs_define
class YouTubeVideoMetadataDTO:
    """
    Attributes:
        views (int):
        likes (int):
        parent (Union['ParentItem', None]):
    """

    views: int
    likes: int
    parent: Union["ParentItem", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.parent_item import ParentItem

        views = self.views

        likes = self.likes

        parent: Union[None, dict[str, Any]]
        if isinstance(self.parent, ParentItem):
            parent = self.parent.to_dict()
        else:
            parent = self.parent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "views": views,
                "likes": likes,
                "parent": parent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parent_item import ParentItem

        d = dict(src_dict)
        views = d.pop("views")

        likes = d.pop("likes")

        def _parse_parent(data: object) -> Union["ParentItem", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                parent_type_0 = ParentItem.from_dict(data)

                return parent_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ParentItem", None], data)

        parent = _parse_parent(d.pop("parent"))

        you_tube_video_metadata_dto = cls(
            views=views,
            likes=likes,
            parent=parent,
        )

        you_tube_video_metadata_dto.additional_properties = d
        return you_tube_video_metadata_dto

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
