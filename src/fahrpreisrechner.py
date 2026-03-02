from __future__ import annotations

from typing import Union

Number = Union[int, float]


def compute_fare(distance_km: Number, age: int, bahncard: int) -> float:
    """
    Fahrpreisrechner (DB-inspiriert).

    Commit 5: Nur Eingabevalidierung (A2).
    - distance_km < 1  -> ValueError
    - age < 0 oder age > 120 -> ValueError
    - bahncard nicht in {0,25,50} -> ValueError

    Die eigentliche Preisberechnung folgt in späteren Commits.
    """
    # Eingabevalidierung nach Anforderungen (A2)
    if distance_km < 1:
        raise ValueError("distance_km must be >= 1")

    if age < 0 or age > 120:
        raise ValueError("age must be between 0 and 120")

    if bahncard not in (0, 25, 50):
        raise ValueError("bahncard must be one of {0, 25, 50}")

    # Platzhalter: Berechnung folgt später
    raise NotImplementedError("price calculation is not implemented yet")
