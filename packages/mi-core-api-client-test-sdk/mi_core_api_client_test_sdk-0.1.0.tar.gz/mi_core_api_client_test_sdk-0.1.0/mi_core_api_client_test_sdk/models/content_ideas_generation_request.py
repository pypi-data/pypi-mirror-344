from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.storyboards_by_channel import StoryboardsByChannel


T = TypeVar("T", bound="ContentIdeasGenerationRequest")


@_attrs_define
class ContentIdeasGenerationRequest:
    """
    Attributes:
        youtube_channels (list['StoryboardsByChannel']):
        storyboard_prompt_id (Union[None, UUID, Unset]):
        scene_img_style_prompt_id (Union[None, UUID, Unset]):
        thumbnail_prompt_id (Union[None, UUID, Unset]):
        scene_img_prompt_id (Union[None, UUID, Unset]):
    """

    youtube_channels: list["StoryboardsByChannel"]
    storyboard_prompt_id: Union[None, UUID, Unset] = UNSET
    scene_img_style_prompt_id: Union[None, UUID, Unset] = UNSET
    thumbnail_prompt_id: Union[None, UUID, Unset] = UNSET
    scene_img_prompt_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        youtube_channels = []
        for youtube_channels_item_data in self.youtube_channels:
            youtube_channels_item = youtube_channels_item_data.to_dict()
            youtube_channels.append(youtube_channels_item)

        storyboard_prompt_id: Union[None, Unset, str]
        if isinstance(self.storyboard_prompt_id, Unset):
            storyboard_prompt_id = UNSET
        elif isinstance(self.storyboard_prompt_id, UUID):
            storyboard_prompt_id = str(self.storyboard_prompt_id)
        else:
            storyboard_prompt_id = self.storyboard_prompt_id

        scene_img_style_prompt_id: Union[None, Unset, str]
        if isinstance(self.scene_img_style_prompt_id, Unset):
            scene_img_style_prompt_id = UNSET
        elif isinstance(self.scene_img_style_prompt_id, UUID):
            scene_img_style_prompt_id = str(self.scene_img_style_prompt_id)
        else:
            scene_img_style_prompt_id = self.scene_img_style_prompt_id

        thumbnail_prompt_id: Union[None, Unset, str]
        if isinstance(self.thumbnail_prompt_id, Unset):
            thumbnail_prompt_id = UNSET
        elif isinstance(self.thumbnail_prompt_id, UUID):
            thumbnail_prompt_id = str(self.thumbnail_prompt_id)
        else:
            thumbnail_prompt_id = self.thumbnail_prompt_id

        scene_img_prompt_id: Union[None, Unset, str]
        if isinstance(self.scene_img_prompt_id, Unset):
            scene_img_prompt_id = UNSET
        elif isinstance(self.scene_img_prompt_id, UUID):
            scene_img_prompt_id = str(self.scene_img_prompt_id)
        else:
            scene_img_prompt_id = self.scene_img_prompt_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "youtube_channels": youtube_channels,
            }
        )
        if storyboard_prompt_id is not UNSET:
            field_dict["storyboard_prompt_id"] = storyboard_prompt_id
        if scene_img_style_prompt_id is not UNSET:
            field_dict["scene_img_style_prompt_id"] = scene_img_style_prompt_id
        if thumbnail_prompt_id is not UNSET:
            field_dict["thumbnail_prompt_id"] = thumbnail_prompt_id
        if scene_img_prompt_id is not UNSET:
            field_dict["scene_img_prompt_id"] = scene_img_prompt_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storyboards_by_channel import StoryboardsByChannel

        d = dict(src_dict)
        youtube_channels = []
        _youtube_channels = d.pop("youtube_channels")
        for youtube_channels_item_data in _youtube_channels:
            youtube_channels_item = StoryboardsByChannel.from_dict(youtube_channels_item_data)

            youtube_channels.append(youtube_channels_item)

        def _parse_storyboard_prompt_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                storyboard_prompt_id_type_0 = UUID(data)

                return storyboard_prompt_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        storyboard_prompt_id = _parse_storyboard_prompt_id(d.pop("storyboard_prompt_id", UNSET))

        def _parse_scene_img_style_prompt_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scene_img_style_prompt_id_type_0 = UUID(data)

                return scene_img_style_prompt_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scene_img_style_prompt_id = _parse_scene_img_style_prompt_id(d.pop("scene_img_style_prompt_id", UNSET))

        def _parse_thumbnail_prompt_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                thumbnail_prompt_id_type_0 = UUID(data)

                return thumbnail_prompt_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        thumbnail_prompt_id = _parse_thumbnail_prompt_id(d.pop("thumbnail_prompt_id", UNSET))

        def _parse_scene_img_prompt_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scene_img_prompt_id_type_0 = UUID(data)

                return scene_img_prompt_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scene_img_prompt_id = _parse_scene_img_prompt_id(d.pop("scene_img_prompt_id", UNSET))

        content_ideas_generation_request = cls(
            youtube_channels=youtube_channels,
            storyboard_prompt_id=storyboard_prompt_id,
            scene_img_style_prompt_id=scene_img_style_prompt_id,
            thumbnail_prompt_id=thumbnail_prompt_id,
            scene_img_prompt_id=scene_img_prompt_id,
        )

        content_ideas_generation_request.additional_properties = d
        return content_ideas_generation_request

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
