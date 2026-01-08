import pytest
from retail import deposit, withdraw


def test_deposit_success(db_with_user):
    new_balance = deposit("u1", db_with_user, 50)
    assert new_balance == 150
    assert db_with_user["u1"]["balance"] == 150
    assert len(db_with_user["u1"]["transaction_history"]) == 1
    assert db_with_user["u1"]["transaction_history"][0]["type"] == "deposit"


def test_deposit_negative_amount(db_with_user):
    with pytest.raises(ValueError):
        deposit("u1", db_with_user, -10)


def test_withdraw_success(db_with_user):
    new_balance = withdraw("u1", db_with_user, 40)
    assert new_balance == 60
    assert db_with_user["u1"]["balance"] == 60
    assert len(db_with_user["u1"]["transaction_history"]) == 1
    assert db_with_user["u1"]["transaction_history"][0]["type"] == "withdraw"


def test_withdraw_not_enough_money(db_with_user):
    with pytest.raises(ValueError):
        withdraw("u1", db_with_user, 1000)
