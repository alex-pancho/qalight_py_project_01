import pytest
from retail import calculate_discount


def test_discount_vip():
    assert calculate_discount(100, "VIP") == 80


def test_discount_student():
    assert calculate_discount(100, "Student") == 90


def test_discount_regular():
    assert calculate_discount(100, "Regular") == 100


def test_discount_invalid_amount():
    with pytest.raises(ValueError):
        calculate_discount(-1, "VIP")
