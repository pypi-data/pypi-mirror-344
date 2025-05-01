from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.serp_search_engine import SerpSearchEngine
from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialArticlesSearchParams")


@_attrs_define
class PartialArticlesSearchParams:
    """
    Attributes:
        engine (Union[None, SerpSearchEngine, Unset]):
        tbm (Union[None, Unset, str]):
        q (Union[None, Unset, list[str]]):
        timeframe (Union[None, Unset, list[str]]):
        num_results (Union[None, Unset, int]):
        offset (Union[None, Unset, int]):
    """

    engine: Union[None, SerpSearchEngine, Unset] = UNSET
    tbm: Union[None, Unset, str] = UNSET
    q: Union[None, Unset, list[str]] = UNSET
    timeframe: Union[None, Unset, list[str]] = UNSET
    num_results: Union[None, Unset, int] = UNSET
    offset: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine: Union[None, Unset, str]
        if isinstance(self.engine, Unset):
            engine = UNSET
        elif isinstance(self.engine, SerpSearchEngine):
            engine = self.engine.value
        else:
            engine = self.engine

        tbm: Union[None, Unset, str]
        if isinstance(self.tbm, Unset):
            tbm = UNSET
        else:
            tbm = self.tbm

        q: Union[None, Unset, list[str]]
        if isinstance(self.q, Unset):
            q = UNSET
        elif isinstance(self.q, list):
            q = self.q

        else:
            q = self.q

        timeframe: Union[None, Unset, list[str]]
        if isinstance(self.timeframe, Unset):
            timeframe = UNSET
        elif isinstance(self.timeframe, list):
            timeframe = self.timeframe

        else:
            timeframe = self.timeframe

        num_results: Union[None, Unset, int]
        if isinstance(self.num_results, Unset):
            num_results = UNSET
        else:
            num_results = self.num_results

        offset: Union[None, Unset, int]
        if isinstance(self.offset, Unset):
            offset = UNSET
        else:
            offset = self.offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if engine is not UNSET:
            field_dict["engine"] = engine
        if tbm is not UNSET:
            field_dict["tbm"] = tbm
        if q is not UNSET:
            field_dict["q"] = q
        if timeframe is not UNSET:
            field_dict["timeframe"] = timeframe
        if num_results is not UNSET:
            field_dict["num_results"] = num_results
        if offset is not UNSET:
            field_dict["offset"] = offset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_engine(data: object) -> Union[None, SerpSearchEngine, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                engine_type_0 = SerpSearchEngine(data)

                return engine_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, SerpSearchEngine, Unset], data)

        engine = _parse_engine(d.pop("engine", UNSET))

        def _parse_tbm(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tbm = _parse_tbm(d.pop("tbm", UNSET))

        def _parse_q(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                q_type_0 = cast(list[str], data)

                return q_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        q = _parse_q(d.pop("q", UNSET))

        def _parse_timeframe(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                timeframe_type_0 = cast(list[str], data)

                return timeframe_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        timeframe = _parse_timeframe(d.pop("timeframe", UNSET))

        def _parse_num_results(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_results = _parse_num_results(d.pop("num_results", UNSET))

        def _parse_offset(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        offset = _parse_offset(d.pop("offset", UNSET))

        partial_articles_search_params = cls(
            engine=engine,
            tbm=tbm,
            q=q,
            timeframe=timeframe,
            num_results=num_results,
            offset=offset,
        )

        partial_articles_search_params.additional_properties = d
        return partial_articles_search_params

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
