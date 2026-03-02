import pytest

# Blackbox-Tests: Grenzwertanalyse (GW)
# Ziel: Übergänge zwischen Klassen prüfen, weil dort typische Fehler auftreten
# (z.B. < statt <=).

from src.fahrpreisrechner import compute_fare

# Für Distanz-Grenzwerte werden Alter und BahnCard konstant gehalten
AGE_FOR_DISTANCE = 30
BC_FOR_DISTANCE = 0

# Für Alters-Grenzwerte werden Distanz und BahnCard konstant gehalten
DIST_FOR_AGE = 100.0  # Basis: 22.00
BC_FOR_AGE = 0


# GW Distanz (6 Fälle)
def test_gw_d1_distance_0_invalid():
    # Grenze: 0 ist ungültig (km < 1)
    with pytest.raises(ValueError):
        compute_fare(0.0, AGE_FOR_DISTANCE, BC_FOR_DISTANCE)


def test_gw_d2_distance_1_first_valid_kurz():
    # Grenze: 1 ist erster gültiger Wert (Kurzstrecke)
    # 5.00 + 1*0.20 = 5.20
    assert compute_fare(1.0, AGE_FOR_DISTANCE, BC_FOR_DISTANCE) == 5.20


def test_gw_d3_distance_50_last_kurz():
    # Grenze: 50 ist letzter Kurzstreckenwert
    # 5.00 + 50*0.20 = 15.00
    assert compute_fare(50.0, AGE_FOR_DISTANCE, BC_FOR_DISTANCE) == 15.00


def test_gw_d4_distance_51_first_mittel():
    # Grenze: 51 ist erster Mittelstreckenwert
    # 8.00 + 51*0.14 = 15.14
    assert compute_fare(51.0, AGE_FOR_DISTANCE, BC_FOR_DISTANCE) == 15.14


def test_gw_d5_distance_200_last_mittel():
    # Grenze: 200 ist letzter Mittelstreckenwert
    # 8.00 + 200*0.14 = 36.00
    assert compute_fare(200.0, AGE_FOR_DISTANCE, BC_FOR_DISTANCE) == 36.00


def test_gw_d6_distance_201_first_lang():
    # Grenze: 201 ist erster Langstreckenwert
    # 12.00 + 201*0.09 = 30.09
    assert compute_fare(201.0, AGE_FOR_DISTANCE, BC_FOR_DISTANCE) == 30.09


# GW Alter (10 Fälle)
def test_gw_a1_age_minus_1_invalid():
    # Grenze: -1 ist ungültig
    with pytest.raises(ValueError):
        compute_fare(DIST_FOR_AGE, -1, BC_FOR_AGE)


def test_gw_a2_age_0_first_free():
    # Grenze: 0 ist erster Kleinkind-Wert (gratis)
    assert compute_fare(DIST_FOR_AGE, 0, BC_FOR_AGE) == 0.00


def test_gw_a3_age_5_last_free():
    # Grenze: 5 ist letzter Kleinkind-Wert (gratis)
    assert compute_fare(DIST_FOR_AGE, 5, BC_FOR_AGE) == 0.00


def test_gw_a4_age_6_first_half():
    # Grenze: 6 ist erster Kind-Wert (50%)
    assert compute_fare(DIST_FOR_AGE, 6, BC_FOR_AGE) == 11.00


def test_gw_a5_age_14_last_half():
    # Grenze: 14 ist letzter Kind-Wert (50%)
    # Besonders wichtig: Grenze 14/15 ist fehleranfällig (off-by-one).
    assert compute_fare(DIST_FOR_AGE, 14, BC_FOR_AGE) == 11.00


def test_gw_a6_age_15_first_adult():
    # Grenze: 15 ist erster Erwachsenen-Wert (0% Rabatt)
    assert compute_fare(DIST_FOR_AGE, 15, BC_FOR_AGE) == 22.00


def test_gw_a7_age_64_last_adult():
    # Grenze: 64 ist letzter Erwachsenen-Wert
    assert compute_fare(DIST_FOR_AGE, 64, BC_FOR_AGE) == 22.00


def test_gw_a8_age_65_first_senior():
    # Grenze: 65 ist erster Senior-Wert (25%)
    assert compute_fare(DIST_FOR_AGE, 65, BC_FOR_AGE) == 16.50


def test_gw_a9_age_120_last_senior():
    # Grenze: 120 ist letzter Senior-Wert (25%)
    assert compute_fare(DIST_FOR_AGE, 120, BC_FOR_AGE) == 16.50


def test_gw_a10_age_121_invalid():
    # Grenze: 121 ist ungültig
    with pytest.raises(ValueError):
        compute_fare(DIST_FOR_AGE, 121, BC_FOR_AGE)
