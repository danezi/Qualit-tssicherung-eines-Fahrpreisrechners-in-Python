from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import math


@dataclass(frozen=True)
class DistanceTariff:
    base: Decimal
    per_km: Decimal


TARIFF_KURZ = DistanceTariff(base=Decimal("5.00"), per_km=Decimal("0.20"))     # 1..50
TARIFF_MITTEL = DistanceTariff(base=Decimal("8.00"), per_km=Decimal("0.14"))   # 51..200
TARIFF_LANG = DistanceTariff(base=Decimal("12.00"), per_km=Decimal("0.09"))    # >200


def _money(amount: Decimal) -> Decimal:
    """Round to cents using commercial rounding."""
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _validate_inputs(distance_km: float, age: int, bahncard: int) -> None:
    if not isinstance(age, int) or isinstance(age, bool):
        raise ValueError("age must be an integer")
    if not isinstance(bahncard, int) or isinstance(bahncard, bool):
        raise ValueError("bahncard must be an integer")

    if not isinstance(distance_km, (int, float)) or isinstance(distance_km, bool):
        raise ValueError("distance_km must be a number")

    if not math.isfinite(float(distance_km)):
        raise ValueError("distance_km must be finite")

    if distance_km < 1:
        raise ValueError("distance_km must be >= 1")

    if age < 0 or age > 120:
        raise ValueError("age must be between 0 and 120")

    if bahncard not in (0, 25, 50):
        raise ValueError("bahncard must be one of {0, 25, 50}")


def _distance_tariff(distance_km: Decimal) -> DistanceTariff:
    if distance_km <= Decimal("50"):
        return TARIFF_KURZ
    if distance_km <= Decimal("200"):
        return TARIFF_MITTEL
    return TARIFF_LANG


def _age_discount(age: int) -> Decimal:
    # 0..5 free
    if 0 <= age <= 5:
        return Decimal("1.00")
    # 6..14 half price
    if 6 <= age <= 14:
        return Decimal("0.50")
    # 15..64 full price
    if 15 <= age <= 64:
        return Decimal("0.00")
    # 65..120 senior discount
    return Decimal("0.25")


def _bahncard_discount(bahncard: int) -> Decimal:
    if bahncard == 0:
        return Decimal("0.00")
    if bahncard == 25:
        return Decimal("0.25")
    return Decimal("0.50")


def compute_fare(distance_km: float, age: int, bahncard: int) -> float:
    """
    Fare rules:
      Preis = (Grundpreis + km * Preis/km) * (1 - Altersrabatt) * (1 - BahnCardRabatt)
    Returns a float rounded to 2 decimals.
    """
    _validate_inputs(distance_km, age, bahncard)

    km = Decimal(str(distance_km))
    age_disc = _age_discount(age)
    bc_disc = _bahncard_discount(bahncard)

    # free ride shortcut (keeps everything clear)
    if age_disc == Decimal("1.00"):
        return 0.00

    tariff = _distance_tariff(km)
    base_price = tariff.base + (km * tariff.per_km)

    final_price = base_price * (Decimal("1.00") - age_disc) * (Decimal("1.00") - bc_disc)
    return float(_money(final_price))