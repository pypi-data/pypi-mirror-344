from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseStoryboardSceneDTO")


@_attrs_define
class BaseStoryboardSceneDTO:
    """
    Attributes:
        scene_number (int):
        title (str):
        timestamp (str):
        heading (str):
        description (str):
        image_url (str):
        id (Union[Unset, UUID]):
    """

    scene_number: int
    title: str
    timestamp: str
    heading: str
    description: str
    image_url: str
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scene_number = self.scene_number

        title = self.title

        timestamp = self.timestamp

        heading = self.heading

        description = self.description

        image_url = self.image_url

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sceneNumber": scene_number,
                "title": title,
                "timestamp": timestamp,
                "heading": heading,
                "description": description,
                "imageUrl": image_url,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scene_number = d.pop("sceneNumber")

        title = d.pop("title")

        timestamp = d.pop("timestamp")

        heading = d.pop("heading")

        description = d.pop("description")

        image_url = d.pop("imageUrl")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        base_storyboard_scene_dto = cls(
            scene_number=scene_number,
            title=title,
            timestamp=timestamp,
            heading=heading,
            description=description,
            image_url=image_url,
            id=id,
        )

        base_storyboard_scene_dto.additional_properties = d
        return base_storyboard_scene_dto

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
