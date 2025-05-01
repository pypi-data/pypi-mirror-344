from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trend_executor import TrendExecutor
from ..types import UNSET, Unset

T = TypeVar("T", bound="RelatedKeywordsRequest")


@_attrs_define
class RelatedKeywordsRequest:
    """
    Attributes:
        type_ (Union[Unset, TrendExecutor]): Enumeration class representing trend executor types.
        prompt_id (Union[None, UUID, Unset]):
    """

    type_: Union[Unset, TrendExecutor] = UNSET
    prompt_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        prompt_id: Union[None, Unset, str]
        if isinstance(self.prompt_id, Unset):
            prompt_id = UNSET
        elif isinstance(self.prompt_id, UUID):
            prompt_id = str(self.prompt_id)
        else:
            prompt_id = self.prompt_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if prompt_id is not UNSET:
            field_dict["prompt_id"] = prompt_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, TrendExecutor]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = TrendExecutor(_type_)

        def _parse_prompt_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                prompt_id_type_0 = UUID(data)

                return prompt_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        prompt_id = _parse_prompt_id(d.pop("prompt_id", UNSET))

        related_keywords_request = cls(
            type_=type_,
            prompt_id=prompt_id,
        )

        related_keywords_request.additional_properties = d
        return related_keywords_request

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
