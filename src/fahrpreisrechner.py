
<<<<<<< feature/step4-skeleton
from typing import Union

Number = Union[int, float]


def _base_price(distance_km: float) -> float:
    """
    Distanzregel (A3): Grundpreis + km * Preis/km

    - 1..50   : 5.00 + 0.20 * km
    - 51..200 : 8.00 + 0.14 * km
    - >200    : 12.00 + 0.09 * km
    """
    if distance_km <= 50:
        return 5.00 + (0.20 * distance_km)
    if distance_km <= 200:
        return 8.00 + (0.14 * distance_km)
    return 12.00 + (0.09 * distance_km)


def _age_discount_factor(age: int) -> float:
    """
    Altersrabatt (A4) als Multiplikator-Faktor (1 - Rabatt).

    - 0..5   : gratis -> Faktor 0.00
    - 6..14  : 50% Rabatt -> Faktor 0.50
    - 15..64 : 0% Rabatt  -> Faktor 1.00
    - 65..120: 25% Rabatt -> Faktor 0.75
    """
    if 0 <= age <= 5:
        return 0.00
    if 6 <= age <= 14:
        return 0.50
    if 15 <= age <= 64:
        return 1.00
    return 0.75


def _bahncard_discount_factor(bahncard: int) -> float:
    """
    BahnCard-Rabatt (A5) als Multiplikator-Faktor (1 - Rabatt).

    - 0  -> Faktor 1.00
    - 25 -> Faktor 0.75
    - 50 -> Faktor 0.50
    """
    if bahncard == 0:
        return 1.00
    if bahncard == 25:
        return 0.75
    return 0.50


def compute_fare(distance_km: Number, age: int, bahncard: int) -> float:
    """
    Fahrpreisrechner (DB-inspiriert).

    Commit 8:
    - Eingabevalidierung (A2)
    - Distanz-Tarif (A3)
    - Altersrabatt (A4)
    - BahnCard-Rabatt (A5)
    - Endpreisformel (A6) mit Rundung auf 2 Dezimalstellen
    """
    # A2 Eingabevalidierung
    if distance_km < 1:
        raise ValueError("distance_km must be >= 1")

    if age < 0 or age > 120:
        raise ValueError("age must be between 0 and 120")

    if bahncard not in (0, 25, 50):
        raise ValueError("bahncard must be one of {0, 25, 50}")

    base = _base_price(float(distance_km))
    age_factor = _age_discount_factor(age)

    # 0..5 Jahre: gratis (unabhängig von BahnCard)
    if age_factor == 0.00:
        return 0.00

    bc_factor = _bahncard_discount_factor(bahncard)

    price = base * age_factor * bc_factor
    return round(price, 2)
=======
>>>>>>> master
