from dataclasses import dataclass


@dataclass(frozen=True)
class SystemConfig:
    system_name: str
    attribute_names: list[str]
    attribute_value_distribution: list[int]
    skill_names: list[str]
    skill_value_distribution: list[int]