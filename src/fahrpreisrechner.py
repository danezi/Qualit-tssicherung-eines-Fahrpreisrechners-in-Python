from __future__ import annotations

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


def compute_fare(distance_km: Number, age: int, bahncard: int) -> float:
    """
    Fahrpreisrechner (DB-inspiriert).

    Commit 6: Distanz-Tarif (A3) + Eingabevalidierung (A2).
    Altersrabatt (A4) und BahnCard-Rabatt (A5) folgen in späteren Commits.

    Aktuelles Verhalten:
    - Ungültige Eingaben -> ValueError
    - Für age=30 und bahncard=0 wird der Distanz-Grundtarif berechnet (rund auf 2 Dezimalstellen)
    - Für andere gültige age/bahncard wird NotImplementedError geworfen (Rabatte noch nicht umgesetzt)
    """
    # A2 Eingabevalidierung
    if distance_km < 1:
        raise ValueError("distance_km must be >= 1")
    if age < 0 or age > 120:
        raise ValueError("age must be between 0 and 120")
    if bahncard not in (0, 25, 50):
        raise ValueError("bahncard must be one of {0, 25, 50}")

    # Commit 6: Nur der Basispreis nach Distanz ist implementiert.
    # Die aktuellen Blackbox-Tests für Distanz nutzen age=30 und bc=0.
    if age != 30 or bahncard != 0:
        raise NotImplementedError("discount rules are not implemented yet")

    price = _base_price(float(distance_km))
    return round(price, 2)
