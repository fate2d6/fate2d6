import json
from pathlib import Path

from fate2d6.models import SystemConfig


def load_config(path: str | Path) -> SystemConfig:
    config_path = Path(path)

    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    system_name = data["system_name"]
    attribute_names = data["attributes"]["names"]
    attribute_value_distribution = data["attributes"]["value_distribution"]
    skill_names = data["skills"]["names"]
    skill_value_distribution = data["skills"]["value_distribution"]

    validate_config(
        system_name=system_name,
        attribute_names=attribute_names,
        attribute_value_distribution=attribute_value_distribution,
        skill_names=skill_names,
        skill_value_distribution=skill_value_distribution,
    )

    return SystemConfig(
        system_name=system_name,
        attribute_names=attribute_names,
        attribute_value_distribution=attribute_value_distribution,
        skill_names=skill_names,
        skill_value_distribution=skill_value_distribution,
    )


def validate_config(
    *,
    system_name: str,
    attribute_names: list[str],
    attribute_value_distribution: list[int],
    skill_names: list[str],
    skill_value_distribution: list[int],
) -> None:
    if not system_name.strip():
        raise ValueError("system_name no puede estar vacío.")

    if len(attribute_names) == 0:
        raise ValueError("Debe haber al menos un atributo.")

    if len(skill_names) == 0:
        raise ValueError("Debe haber al menos una habilidad.")

    if len(attribute_names) != len(attribute_value_distribution):
        raise ValueError(
            "El número de nombres de atributos debe coincidir con la longitud "
            "de attribute_value_distribution."
        )

    if len(skill_names) != len(skill_value_distribution):
        raise ValueError(
            "El número de nombres de habilidades debe coincidir con la longitud "
            "de skill_value_distribution."
        )

    if len(set(attribute_names)) != len(attribute_names):
        raise ValueError("Hay nombres de atributos duplicados.")

    if len(set(skill_names)) != len(skill_names):
        raise ValueError("Hay nombres de habilidades duplicados.")
