from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.assessment_type import AssessmentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="StoryboardAssessmentRequest")


@_attrs_define
class StoryboardAssessmentRequest:
    """
    Attributes:
        comment (Union[None, Unset, str]):
        assessment (Union[AssessmentType, None, Unset]):
    """

    comment: Union[None, Unset, str] = UNSET
    assessment: Union[AssessmentType, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comment is not UNSET:
            field_dict["comment"] = comment
        if assessment is not UNSET:
            field_dict["assessment"] = assessment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

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

        storyboard_assessment_request = cls(
            comment=comment,
            assessment=assessment,
        )

        storyboard_assessment_request.additional_properties = d
        return storyboard_assessment_request

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
