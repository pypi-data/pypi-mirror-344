from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.serp_search_engine import SerpSearchEngine

T = TypeVar("T", bound="ArticlesSearchParams")


@_attrs_define
class ArticlesSearchParams:
    """
    Attributes:
        engine (SerpSearchEngine): Enumeration class representing SERP search engines.
        tbm (str):
        q (list[str]):
        timeframe (list[str]):
        num_results (int):
        offset (int):
    """

    engine: SerpSearchEngine
    tbm: str
    q: list[str]
    timeframe: list[str]
    num_results: int
    offset: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine = self.engine.value

        tbm = self.tbm

        q = self.q

        timeframe = self.timeframe

        num_results = self.num_results

        offset = self.offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engine": engine,
                "tbm": tbm,
                "q": q,
                "timeframe": timeframe,
                "num_results": num_results,
                "offset": offset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        engine = SerpSearchEngine(d.pop("engine"))

        tbm = d.pop("tbm")

        q = cast(list[str], d.pop("q"))

        timeframe = cast(list[str], d.pop("timeframe"))

        num_results = d.pop("num_results")

        offset = d.pop("offset")

        articles_search_params = cls(
            engine=engine,
            tbm=tbm,
            q=q,
            timeframe=timeframe,
            num_results=num_results,
            offset=offset,
        )

        articles_search_params.additional_properties = d
        return articles_search_params

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
