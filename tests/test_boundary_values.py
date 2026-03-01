import pytest

from src.fahrpreisrechner import compute_fare


# Pour les frontières distance, on garde age/bc constants
AGE = 30
BC = 0

# Pour les frontières age, on garde distance/bc constants
DIST = 100.0
BC_AGE = 0


# -------------------------
# Distance boundaries (6 cases)
# -------------------------

def test_gw_distance_0_invalid():
    with pytest.raises(ValueError):
        compute_fare(0.0, AGE, BC)


def test_gw_distance_1_valid_kurz():
    # 1 => 5 + 1*0.20 = 5.20
    assert compute_fare(1.0, AGE, BC) == 5.20


def test_gw_distance_50_last_kurz():
    # 50 => 5 + 50*0.20 = 15.00
    assert compute_fare(50.0, AGE, BC) == 15.00


def test_gw_distance_51_first_mittel():
    # 51 => 8 + 51*0.14 = 15.14
    assert compute_fare(51.0, AGE, BC) == 15.14


def test_gw_distance_200_last_mittel():
    # 200 => 8 + 200*0.14 = 36.00
    assert compute_fare(200.0, AGE, BC) == 36.00


def test_gw_distance_201_first_lang():
    # 201 => 12 + 201*0.09 = 30.09
    assert compute_fare(201.0, AGE, BC) == 30.09


# -------------------------
# Age boundaries (10 cases)
# -------------------------

def test_gw_age_minus_1_invalid():
    with pytest.raises(ValueError):
        compute_fare(DIST, -1, BC_AGE)


def test_gw_age_0_free():
    assert compute_fare(DIST, 0, BC_AGE) == 0.00


def test_gw_age_5_last_free():
    assert compute_fare(DIST, 5, BC_AGE) == 0.00


def test_gw_age_6_first_half():
    assert compute_fare(DIST, 6, BC_AGE) == 11.00


def test_gw_age_14_last_half():
    assert compute_fare(DIST, 14, BC_AGE) == 11.00


def test_gw_age_15_first_adult():
    assert compute_fare(DIST, 15, BC_AGE) == 22.00


def test_gw_age_64_last_adult():
    assert compute_fare(DIST, 64, BC_AGE) == 22.00


def test_gw_age_65_first_senior():
    assert compute_fare(DIST, 65, BC_AGE) == 16.50


def test_gw_age_120_last_senior():
    assert compute_fare(DIST, 120, BC_AGE) == 16.50


def test_gw_age_121_invalid():
    with pytest.raises(ValueError):
        compute_fare(DIST, 121, BC_AGE)