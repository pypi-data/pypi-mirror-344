from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.search_bar_type import SearchBarType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchbarItemDTO")


@_attrs_define
class SearchbarItemDTO:
    """
    Attributes:
        name (str):
        handle (str):
        subscribers (int):
        logo_url (str):
        type_ (SearchBarType): Enumeration class representing search bar type options.

            Attributes:
                CHANNEL: Represents channel search bar type option.
                SUBREDDIT: Represents subreddit search bar type option.
        id (Union[Unset, UUID]):
    """

    name: str
    handle: str
    subscribers: int
    logo_url: str
    type_: SearchBarType
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        handle = self.handle

        subscribers = self.subscribers

        logo_url = self.logo_url

        type_ = self.type_.value

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "handle": handle,
                "subscribers": subscribers,
                "logoUrl": logo_url,
                "type": type_,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        handle = d.pop("handle")

        subscribers = d.pop("subscribers")

        logo_url = d.pop("logoUrl")

        type_ = SearchBarType(d.pop("type"))

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = UUID(_id)

        searchbar_item_dto = cls(
            name=name,
            handle=handle,
            subscribers=subscribers,
            logo_url=logo_url,
            type_=type_,
            id=id,
        )

        searchbar_item_dto.additional_properties = d
        return searchbar_item_dto

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
