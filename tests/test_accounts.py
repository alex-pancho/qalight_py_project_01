import pytest
from retail import create_account


def test_create_account_success(db_empty):
    balance = create_account("u1", db_empty, 100)
    assert balance == 100
    assert "u1" in db_empty
    assert db_empty["u1"]["balance"] == 100


def test_create_account_duplicate(db_with_user):
    with pytest.raises(ValueError):
        create_account("u1", db_with_user, 50)
