from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.assessment_type import AssessmentType
from ..models.storyboard_generation_status_enum import StoryboardGenerationStatusEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_storyboard_scene_dto import BaseStoryboardSceneDTO


T = TypeVar("T", bound="StoryboardAssessmentResponse")


@_attrs_define
class StoryboardAssessmentResponse:
    """
    Attributes:
        title (Union[None, str]):
        thumbnail_url (Union[None, str]):
        archetype (Union[None, UUID]):
        scenes (list['BaseStoryboardSceneDTO']):
        comment (Union[None, Unset, str]):
        assessment (Union[AssessmentType, None, Unset]):
        id (Union[Unset, UUID]):
        status (Union[Unset, StoryboardGenerationStatusEnum]): Enumeration class representing storyboard generation
            status.
    """

    title: Union[None, str]
    thumbnail_url: Union[None, str]
    archetype: Union[None, UUID]
    scenes: list["BaseStoryboardSceneDTO"]
    comment: Union[None, Unset, str] = UNSET
    assessment: Union[AssessmentType, None, Unset] = UNSET
    id: Union[Unset, UUID] = UNSET
    status: Union[Unset, StoryboardGenerationStatusEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: Union[None, str]
        title = self.title

        thumbnail_url: Union[None, str]
        thumbnail_url = self.thumbnail_url

        archetype: Union[None, str]
        if isinstance(self.archetype, UUID):
            archetype = str(self.archetype)
        else:
            archetype = self.archetype

        scenes = []
        for scenes_item_data in self.scenes:
            scenes_item = scenes_item_data.to_dict()
            scenes.append(scenes_item)

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        assessment: Union[None, Unset, str]
        if isinstance(self.assessment, Unset):
            assessment = UNSET
        elif isinstance(self.assessment, AssessmentType):
            assessment = self.assessment.value
        else:
            assessment = self.assessment

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "thumbnailUrl": thumbnail_url,
                "archetype": archetype,
                "scenes": scenes,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if assessment is not UNSET:
            field_dict["assessment"] = assessment
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_storyboard_scene_dto import BaseStoryboardSceneDTO

        d = dict(src_dict)

        def _parse_title(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        title = _parse_title(d.pop("title"))

        def _parse_thumbnail_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        thumbnail_url = _parse_thumbnail_url(d.pop("thumbnailUrl"))

        def _parse_archetype(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                archetype_type_0 = UUID(data)

                return archetype_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        archetype = _parse_archetype(d.pop("archetype"))

        scenes = []
        _scenes = d.pop("scenes")
        for scenes_item_data in _scenes:
            scenes_item = BaseStoryboardSceneDTO.from_dict(scenes_item_data)

            scenes.append(scenes_item)

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_assessment(data: object) -> Union[AssessmentType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                assessment_type_0 = AssessmentType(data)

                return assessment_type_0
            except:  # noqa: E722
                pass
            return cast(Union[AssessmentType, None, Unset], data)

        assessment = _parse_assessment(d.pop("assessment", UNSET))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        _status = d.pop("status", UNSET)
        status: Union[Unset, StoryboardGenerationStatusEnum]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = StoryboardGenerationStatusEnum(_status)

        storyboard_assessment_response = cls(
            title=title,
            thumbnail_url=thumbnail_url,
            archetype=archetype,
            scenes=scenes,
            comment=comment,
            assessment=assessment,
            id=id,
            status=status,
        )

        storyboard_assessment_response.additional_properties = d
        return storyboard_assessment_response

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
