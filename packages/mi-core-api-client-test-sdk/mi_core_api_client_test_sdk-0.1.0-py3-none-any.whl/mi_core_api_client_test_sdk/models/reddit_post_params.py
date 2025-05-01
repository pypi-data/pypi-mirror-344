from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RedditPostParams")


@_attrs_define
class RedditPostParams:
    """
    Attributes:
        with_comments (Union[Unset, bool]):  Default: False.
        max_duration_sec (Union[Unset, int]):  Default: 60.
    """

    with_comments: Union[Unset, bool] = False
    max_duration_sec: Union[Unset, int] = 60
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        with_comments = self.with_comments

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
        with_comments = d.pop("with_comments", UNSET)

        max_duration_sec = d.pop("max_duration_sec", UNSET)

        reddit_post_params = cls(
            with_comments=with_comments,
            max_duration_sec=max_duration_sec,
        )

        reddit_post_params.additional_properties = d
        return reddit_post_params

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
