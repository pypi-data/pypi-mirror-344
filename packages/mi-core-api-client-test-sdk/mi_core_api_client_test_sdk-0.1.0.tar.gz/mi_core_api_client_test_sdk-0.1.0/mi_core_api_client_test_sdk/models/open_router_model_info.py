from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_architecture import ModelArchitecture
    from ..models.open_router_model_info_per_request_limits_type_0 import OpenRouterModelInfoPerRequestLimitsType0
    from ..models.pricing import Pricing
    from ..models.top_provider import TopProvider


T = TypeVar("T", bound="OpenRouterModelInfo")


@_attrs_define
class OpenRouterModelInfo:
    """
    Attributes:
        id (str):
        name (str):
        created (float):
        description (str):
        architecture (ModelArchitecture):
        top_provider (TopProvider):
        pricing (Pricing):
        context_length (Union[None, Unset, float]):
        per_request_limits (Union['OpenRouterModelInfoPerRequestLimitsType0', None, Unset]):
    """

    id: str
    name: str
    created: float
    description: str
    architecture: "ModelArchitecture"
    top_provider: "TopProvider"
    pricing: "Pricing"
    context_length: Union[None, Unset, float] = UNSET
    per_request_limits: Union["OpenRouterModelInfoPerRequestLimitsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.open_router_model_info_per_request_limits_type_0 import OpenRouterModelInfoPerRequestLimitsType0

        id = self.id

        name = self.name

        created = self.created

        description = self.description

        architecture = self.architecture.to_dict()

        top_provider = self.top_provider.to_dict()

        pricing = self.pricing.to_dict()

        context_length: Union[None, Unset, float]
        if isinstance(self.context_length, Unset):
            context_length = UNSET
        else:
            context_length = self.context_length

        per_request_limits: Union[None, Unset, dict[str, Any]]
        if isinstance(self.per_request_limits, Unset):
            per_request_limits = UNSET
        elif isinstance(self.per_request_limits, OpenRouterModelInfoPerRequestLimitsType0):
            per_request_limits = self.per_request_limits.to_dict()
        else:
            per_request_limits = self.per_request_limits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "created": created,
                "description": description,
                "architecture": architecture,
                "topProvider": top_provider,
                "pricing": pricing,
            }
        )
        if context_length is not UNSET:
            field_dict["contextLength"] = context_length
        if per_request_limits is not UNSET:
            field_dict["perRequestLimits"] = per_request_limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_architecture import ModelArchitecture
        from ..models.open_router_model_info_per_request_limits_type_0 import OpenRouterModelInfoPerRequestLimitsType0
        from ..models.pricing import Pricing
        from ..models.top_provider import TopProvider

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        created = d.pop("created")

        description = d.pop("description")

        architecture = ModelArchitecture.from_dict(d.pop("architecture"))

        top_provider = TopProvider.from_dict(d.pop("topProvider"))

        pricing = Pricing.from_dict(d.pop("pricing"))

        def _parse_context_length(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        context_length = _parse_context_length(d.pop("contextLength", UNSET))

        def _parse_per_request_limits(data: object) -> Union["OpenRouterModelInfoPerRequestLimitsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                per_request_limits_type_0 = OpenRouterModelInfoPerRequestLimitsType0.from_dict(data)

                return per_request_limits_type_0
            except:  # noqa: E722
                pass
            return cast(Union["OpenRouterModelInfoPerRequestLimitsType0", None, Unset], data)

        per_request_limits = _parse_per_request_limits(d.pop("perRequestLimits", UNSET))

        open_router_model_info = cls(
            id=id,
            name=name,
            created=created,
            description=description,
            architecture=architecture,
            top_provider=top_provider,
            pricing=pricing,
            context_length=context_length,
            per_request_limits=per_request_limits,
        )

        open_router_model_info.additional_properties = d
        return open_router_model_info

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
