from collections import Counter
import math

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


def modifier_mode(config: SystemConfig) -> int:
    """
    Devuelve la moda de la distribución de modificadores.
    """
    distribution = modifier_distribution(config)
    return max(distribution, key=distribution.get)


def modifier_variance(config: SystemConfig) -> float:
    """
    Calcula la varianza de la distribución de modificadores.
    """
    probabilities = modifier_probabilities(config)
    mean = expected_modifier(config)

    return sum(
        probability * (modifier - mean) ** 2
        for modifier, probability in probabilities.items()
    )


def modifier_std(config: SystemConfig) -> float:
    """
    Calcula la desviación típica de la distribución de modificadores.
    """
    return math.sqrt(modifier_variance(config))

def two_d6_distribution() -> dict[int, int]:
    """
    Calcula la distribución exacta de frecuencias de 2d6.

    Devuelve un diccionario {resultado: frecuencia}.
    """
    distribution: Counter[int] = Counter()

    for die_1 in range(1, 7):
        for die_2 in range(1, 7):
            total = die_1 + die_2
            distribution[total] += 1

    return dict(sorted(distribution.items()))


def two_d6_probabilities() -> dict[int, float]:
    """
    Calcula la distribución exacta de probabilidades de 2d6.

    Devuelve un diccionario {resultado: probabilidad}.
    """
    distribution = two_d6_distribution()
    total_combinations = sum(distribution.values())

    return {
        result: frequency / total_combinations
        for result, frequency in distribution.items()
    }


def expected_two_d6() -> float:
    """
    Calcula el valor esperado de 2d6.
    """
    probabilities = two_d6_probabilities()

    return sum(
        result * probability
        for result, probability in probabilities.items()
    )


def two_d6_mode() -> int:
    """
    Devuelve la moda de la distribución de 2d6.
    """
    distribution = two_d6_distribution()
    return max(distribution, key=distribution.get)


def two_d6_variance() -> float:
    """
    Calcula la varianza de la distribución de 2d6.
    """
    probabilities = two_d6_probabilities()
    mean = expected_two_d6()

    return sum(
        probability * (result - mean) ** 2
        for result, probability in probabilities.items()
    )


def two_d6_std() -> float:
    """
    Calcula la desviación típica de la distribución de 2d6.
    """
    return math.sqrt(two_d6_variance())

def shifted_two_d6_distribution(shift: float) -> dict[float, float]:
    """
    Desplaza la distribución de 2d6 por un valor dado.

    Devuelve un diccionario {resultado_desplazado: probabilidad}.
    """
    base_probabilities = two_d6_probabilities()

    return {
        result + shift: probability
        for result, probability in base_probabilities.items()
    }


def probability_at_least(distribution: dict[float, float], threshold: float) -> float:
    """
    Calcula la probabilidad de obtener al menos un valor dado
    en una distribución discreta.
    """
    return sum(
        probability
        for result, probability in distribution.items()
        if result >= threshold
    )

def shifted_two_d6_distribution(shift: int | float) -> dict[float, float]:
    """
    Desplaza la distribución de 2d6 por un valor dado.

    Devuelve un diccionario {resultado_desplazado: probabilidad}.
    """
    base_probabilities = two_d6_probabilities()

    return {
        result + shift: probability
        for result, probability in base_probabilities.items()
    }


def probability_at_least(
    distribution: dict[int | float, float],
    threshold: int | float,
) -> float:
    """
    Calcula la probabilidad de obtener al menos un valor dado
    en una distribución discreta.
    """
    return sum(
        probability
        for result, probability in distribution.items()
        if result >= threshold
    )


def expected_shifted_two_d6(shift: int | float) -> float:
    """
    Calcula el valor esperado de 2d6 desplazado por un modificador dado.
    """
    return expected_two_d6() + shift

def probability_with_reroll(p_success: float) -> float:
    """
    Calcula la probabilidad de éxito al permitir un reroll completo.

    p_success: probabilidad de éxito en una tirada normal

    Devuelve:
    P(éxito en 1ª o en 2ª) = p + (1 - p)*p = 1 - (1 - p)^2
    """
    return 1 - (1 - p_success) ** 2