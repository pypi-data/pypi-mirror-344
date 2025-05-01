from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TopProvider")


@_attrs_define
class TopProvider:
    """
    Attributes:
        is_moderated (bool):
        context_length (Union[None, Unset, float]):
        max_completion_tokens (Union[None, Unset, float]):
    """

    is_moderated: bool
    context_length: Union[None, Unset, float] = UNSET
    max_completion_tokens: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_moderated = self.is_moderated

        context_length: Union[None, Unset, float]
        if isinstance(self.context_length, Unset):
            context_length = UNSET
        else:
            context_length = self.context_length

        max_completion_tokens: Union[None, Unset, float]
        if isinstance(self.max_completion_tokens, Unset):
            max_completion_tokens = UNSET
        else:
            max_completion_tokens = self.max_completion_tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isModerated": is_moderated,
            }
        )
        if context_length is not UNSET:
            field_dict["contextLength"] = context_length
        if max_completion_tokens is not UNSET:
            field_dict["maxCompletionTokens"] = max_completion_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_moderated = d.pop("isModerated")

        def _parse_context_length(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        context_length = _parse_context_length(d.pop("contextLength", UNSET))

        def _parse_max_completion_tokens(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        max_completion_tokens = _parse_max_completion_tokens(d.pop("maxCompletionTokens", UNSET))

        top_provider = cls(
            is_moderated=is_moderated,
            context_length=context_length,
            max_completion_tokens=max_completion_tokens,
        )

        top_provider.additional_properties = d
        return top_provider

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
