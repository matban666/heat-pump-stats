import pytest
from utils.calculations import cop, power_from_flow

def test_cop():
    assert cop(3, 3) == 1
    assert cop(3, 9) == 3
    assert cop(0, 3) == 0

def test_power_from_flow():
    assert power_from_flow(30, 5) == 10.466999999999999
    assert power_from_flow(12, 4) == 3.34944
    assert power_from_flow(0, 3) == 0