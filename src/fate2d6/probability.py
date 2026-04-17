from collections import Counter

from fate2d6.models import SystemConfig


def modifier_distribution(config: SystemConfig) -> dict[int, int]:
    """
    Calcula la distribución de frecuencias de Atributo + Habilidad
    para la configuración dada.

    Devuelve un diccionario {resultado: frecuencia}.
    """
    distribution: Counter[int] = Counter()

    for attribute_value in config.attribute_value_distribution:
        for skill_value in config.skill_value_distribution:
            total_modifier = attribute_value + skill_value
            distribution[total_modifier] += 1

    return dict(sorted(distribution.items()))


def modifier_probabilities(config: SystemConfig) -> dict[int, float]:
    """
    Calcula la distribución de probabilidades de Atributo + Habilidad
    para la configuración dada.

    Devuelve un diccionario {resultado: probabilidad}.
    """
    distribution = modifier_distribution(config)
    total_combinations = sum(distribution.values())

    return {
        modifier: frequency / total_combinations
        for modifier, frequency in distribution.items()
    }


def total_modifier_combinations(config: SystemConfig) -> int:
    """
    Devuelve el número total de combinaciones Atributo x Habilidad.
    """
    return (
        len(config.attribute_value_distribution)
        * len(config.skill_value_distribution)
    )


def expected_modifier(config: SystemConfig) -> float:
    """
    Calcula el valor esperado del modificador Atributo + Habilidad.
    """
    probabilities = modifier_probabilities(config)

    return sum(
        modifier * probability
        for modifier, probability in probabilities.items()
    )
