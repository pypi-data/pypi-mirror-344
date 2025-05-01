from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Pricing")


@_attrs_define
class Pricing:
    """
    Attributes:
        prompt (str):
        completion (str):
        image (str):
        request (str):
        web_search (str):
        internal_reasoning (str):
        input_cache_read (Union[None, Unset, str]):
        input_cache_write (Union[None, Unset, str]):
    """

    prompt: str
    completion: str
    image: str
    request: str
    web_search: str
    internal_reasoning: str
    input_cache_read: Union[None, Unset, str] = UNSET
    input_cache_write: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        completion = self.completion

        image = self.image

        request = self.request

        web_search = self.web_search

        internal_reasoning = self.internal_reasoning

        input_cache_read: Union[None, Unset, str]
        if isinstance(self.input_cache_read, Unset):
            input_cache_read = UNSET
        else:
            input_cache_read = self.input_cache_read

        input_cache_write: Union[None, Unset, str]
        if isinstance(self.input_cache_write, Unset):
            input_cache_write = UNSET
        else:
            input_cache_write = self.input_cache_write

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
                "completion": completion,
                "image": image,
                "request": request,
                "webSearch": web_search,
                "internalReasoning": internal_reasoning,
            }
        )
        if input_cache_read is not UNSET:
            field_dict["inputCacheRead"] = input_cache_read
        if input_cache_write is not UNSET:
            field_dict["inputCacheWrite"] = input_cache_write

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        prompt = d.pop("prompt")

        completion = d.pop("completion")

        image = d.pop("image")

        request = d.pop("request")

        web_search = d.pop("webSearch")

        internal_reasoning = d.pop("internalReasoning")

        def _parse_input_cache_read(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_cache_read = _parse_input_cache_read(d.pop("inputCacheRead", UNSET))

        def _parse_input_cache_write(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        input_cache_write = _parse_input_cache_write(d.pop("inputCacheWrite", UNSET))

        pricing = cls(
            prompt=prompt,
            completion=completion,
            image=image,
            request=request,
            web_search=web_search,
            internal_reasoning=internal_reasoning,
            input_cache_read=input_cache_read,
            input_cache_write=input_cache_write,
        )

        pricing.additional_properties = d
        return pricing

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
