from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SavingsStatisticlbsCO2E")


@_attrs_define
class SavingsStatisticlbsCO2E:
    """
    Attributes:
        lower (float): **Unit:** lbsCO2e/ft2
        estimate (float): **Unit:** lbsCO2e/ft2
        upper (float): **Unit:** lbsCO2e/ft2
    """

    lower: float
    estimate: float
    upper: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lower = self.lower

        estimate = self.estimate

        upper = self.upper

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "lower": lower,
            "estimate": estimate,
            "upper": upper,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lower = d.pop("lower")

        estimate = d.pop("estimate")

        upper = d.pop("upper")

        savings_statisticlbs_co2e = cls(
            lower=lower,
            estimate=estimate,
            upper=upper,
        )

        savings_statisticlbs_co2e.additional_properties = d
        return savings_statisticlbs_co2e

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
