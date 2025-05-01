from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialRedditPostParams")


@_attrs_define
class PartialRedditPostParams:
    """
    Attributes:
        with_comments (Union[None, Unset, bool]):
        max_duration_sec (Union[None, Unset, int]):
    """

    with_comments: Union[None, Unset, bool] = UNSET
    max_duration_sec: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        with_comments: Union[None, Unset, bool]
        if isinstance(self.with_comments, Unset):
            with_comments = UNSET
        else:
            with_comments = self.with_comments

        max_duration_sec: Union[None, Unset, int]
        if isinstance(self.max_duration_sec, Unset):
            max_duration_sec = UNSET
        else:
            max_duration_sec = self.max_duration_sec

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if with_comments is not UNSET:
            field_dict["with_comments"] = with_comments
        if max_duration_sec is not UNSET:
            field_dict["max_duration_sec"] = max_duration_sec

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_with_comments(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        with_comments = _parse_with_comments(d.pop("with_comments", UNSET))

        def _parse_max_duration_sec(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_duration_sec = _parse_max_duration_sec(d.pop("max_duration_sec", UNSET))

        partial_reddit_post_params = cls(
            with_comments=with_comments,
            max_duration_sec=max_duration_sec,
        )

        partial_reddit_post_params.additional_properties = d
        return partial_reddit_post_params

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
