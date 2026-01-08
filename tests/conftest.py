import pytest
import retail


@pytest.fixture
def db_empty():
    return {}


@pytest.fixture
def db_with_user():
    return {
        "u1": {
            "balance": 100.0,
            "category": "Regular",
            "transaction_history": []
        }
    }


@pytest.fixture(autouse=True)
def no_real_file_io(monkeypatch):
    """
    Автоматично для всіх тестів:
    - відключаємо реальний запис у accounts.json
    """
    monkeypatch.setattr(retail.db, "save_database", lambda *args, **kwargs: None)
