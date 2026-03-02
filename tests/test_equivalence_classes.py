import pytest

# Blackbox-Tests: Äquivalenzklassenbildung (EK)
# Ziel: Unendlichen Eingaberaum in Klassen mit gleichem Verhalten partitionieren.
# Pro Klasse genügt ein repräsentativer Testwert (weit weg von Grenzwerten).

from src.fahrpreisrechner import compute_fare

# Neutrale, gültige Standardwerte (keine Rabatte), um jeweils nur eine Dimension zu testen
NEUTRAL_DISTANCE = 100.0  # Mittelstrecke: 8.00 + 100*0.14 = 22.00
NEUTRAL_AGE = 30          # Erwachsener: 0% Altersrabatt
NEUTRAL_BC = 0            # Keine BahnCard: 0% BahnCard-Rabatt


# EK Distanz (4 Klassen)
def test_ek_d0_distance_invalid_under_1km():
    # EK-D0: Ungültig (km < 1)
    with pytest.raises(ValueError):
        compute_fare(0.5, NEUTRAL_AGE, NEUTRAL_BC)


def test_ek_d1_kurzstrecke_typical():
    # EK-D1: Kurzstrecke (1..50), repräsentativer Wert: 25 km
    # Erwartung: 5.00 + 25*0.20 = 10.00
    assert compute_fare(25.0, NEUTRAL_AGE, NEUTRAL_BC) == 10.00


def test_ek_d2_mittelstrecke_typical():
    # EK-D2: Mittelstrecke (51..200), repräsentativer Wert: 100 km
    # Erwartung: 8.00 + 100*0.14 = 22.00
    assert compute_fare(100.0, NEUTRAL_AGE, NEUTRAL_BC) == 22.00


def test_ek_d3_langstrecke_typical():
    # EK-D3: Langstrecke (>200), repräsentativer Wert: 300 km
    # Erwartung: 12.00 + 300*0.09 = 39.00
    assert compute_fare(300.0, NEUTRAL_AGE, NEUTRAL_BC) == 39.00


# EK Alter (5 Klassen)
def test_ek_a0_age_invalid_negative():
    # EK-A0: Ungültig (age < 0 oder age > 120)
    with pytest.raises(ValueError):
        compute_fare(NEUTRAL_DISTANCE, -1, NEUTRAL_BC)


def test_ek_a1_kleinkind_free():
    # EK-A1: Kleinkind (0..5) => 100% Rabatt => 0.00
    assert compute_fare(NEUTRAL_DISTANCE, 3, NEUTRAL_BC) == 0.00


def test_ek_a2_kind_50_percent():
    # EK-A2: Kind (6..14) => 50% Rabatt
    # Basis bei 100 km: 22.00 => 11.00
    assert compute_fare(NEUTRAL_DISTANCE, 10, NEUTRAL_BC) == 11.00


def test_ek_a3_erwachsener_full_price():
    # EK-A3: Erwachsener (15..64) => 0% Rabatt
    assert compute_fare(NEUTRAL_DISTANCE, 30, NEUTRAL_BC) == 22.00


def test_ek_a4_senior_25_percent():
    # EK-A4: Senior (65..120) => 25% Rabatt
    # 22.00 * 0.75 = 16.50
    assert compute_fare(NEUTRAL_DISTANCE, 70, NEUTRAL_BC) == 16.50


# EK BahnCard (4 Klassen)
def test_ek_b0_bahncard_invalid_value():
    # EK-B0: Ungültig (bc nicht in {0,25,50})
    with pytest.raises(ValueError):
        compute_fare(NEUTRAL_DISTANCE, NEUTRAL_AGE, 10)


def test_ek_b1_no_bahncard():
    # EK-B1: Keine BahnCard (bc=0) => 0% Rabatt
    assert compute_fare(NEUTRAL_DISTANCE, NEUTRAL_AGE, 0) == 22.00


def test_ek_b2_bahncard_25():
    # EK-B2: BahnCard 25 => 25% Rabatt
    # 22.00 * 0.75 = 16.50
    assert compute_fare(NEUTRAL_DISTANCE, NEUTRAL_AGE, 25) == 16.50


def test_ek_b3_bahncard_50():
    # EK-B3: BahnCard 50 => 50% Rabatt
    # 22.00 * 0.50 = 11.00
    assert compute_fare(NEUTRAL_DISTANCE, NEUTRAL_AGE, 50) == 11.00
