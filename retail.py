
import database as db

def create_account(bayer_id: str, database: dict, initial_balance: float = 0):
    """
    Створює новий рахунок прив'язаний до bayer_id - ід покупця.

    Args:
        bayer_id (str): Ід власника рахунку
        database (dict): Завантажена база даних
        initial_balance (float): Початковий баланс (за замовчуванням 0)

    Returns:
        float: Початковий баланс створеного рахунку

    Raises:
        ValueError: Якщо ім'я порожнє або баланс від'ємний
    """
    if bayer_id in database:
        raise ValueError(f"Рахунок з ID '{bayer_id}' вже існує")

    account = {
        "bayer_id": bayer_id,
        "balance": initial_balance,
        "category": "Regular",
        "transaction_history": [],
    }
    # Додаємо рахунок до бази
    database[bayer_id] = account
    db.save_database(database)

    print(f"✓ Рахунок '{bayer_id}' успішно створено")
    return initial_balance


def get_balance(bayer_id: str, database: dict):
    """
    Повертає поточний баланс рахунку.

    Args:
        bayer_id (str): ID покупця

    Returns:
        float: Поточний баланс

    Raises:
        ValueError: Якщо рахунок не знайдено
    """
    if bayer_id not in database:
        raise ValueError(f"Рахунок з ID '{bayer_id}' не знайдено")
    return database[bayer_id]["balance"]


def deposit(bayer_id: str, database:dict, amount: float):
    """
    Docstring for deposit
    
    :param bayer_id: Description
    :type bayer_id: str
    :param database: Description
    :type database: dict
    :param amount: Description
    :type amount: float
    """
    if bayer_id not in database:
        raise ValueError(f"Рахунок з ID '{bayer_id}' не знайдено")
    database[bayer_id]["balance"] += amount
    
    transaction = {
        "type": "deposit",
        "amount": amount,
        "balance_after": database[bayer_id]["balance"],
    }
    database[bayer_id]["transaction_history"].append(transaction)

    db.save_database(database)
    new_balance = database[bayer_id]["balance"]
    print(
        f"✓ Рахунок поповнено на {amount:.2f} грн. Новий баланс: {new_balance:.2f} грн"
    )

    return new_balance


def withdraw(bayer_id: str, database:dict, amount: float):
    """
    Docstring for deposit
    
    :param bayer_id: Description
    :type bayer_id: str
    :param database: Description
    :type database: dict
    :param amount: Description
    :type amount: float
    """
    if bayer_id not in database:
        raise ValueError(f"Рахунок з ID '{bayer_id}' не знайдено")
    database[bayer_id]["balance"] -= amount
    
    transaction = {
        "type": "withdraw",
        "amount": amount,
        "balance_after": database[bayer_id]["balance"],
    }
    database[bayer_id]["transaction_history"].append(transaction)

    db.save_database(database)
    new_balance = database[bayer_id]["balance"]
    print(
        f"✓ Виведено з рахунку {amount:.2f} грн. Новий баланс: {new_balance:.2f} грн"
    )

    return new_balance


def calculate_discount(price, category):
    """
    Нараховує знижку залежно від категорії клієнта.

    Args:
        price (float): Початкова ціна товару
        category (str): Категорія клієнта ('VIP', 'Student' або інше)

    Returns:
        float: Ціна після знижки

    Raises:
        ValueError: Якщо ціна від'ємна
        TypeError: Якщо ціна не є числом

    Знижки:
        - VIP: 20% (множимо на 0.8)
        - Student: 10% (множимо на 0.9)
        - Інші: 0% (без змін)
    """
    # Перевірка типу
    if not isinstance(price, (int, float)):
        raise TypeError("Ціна повинна бути числом")

    # Перевірка на від'ємне значення
    if price < 0:
        raise ValueError("Ціна не може бути від'ємною")

    # Нормалізуємо категорію до верхнього регістру для порівняння
    category_upper = category.upper().strip()

    # Застосовуємо знижку залежно від категорії
    if category_upper == "VIP":
        return price * 0.8  # 20% знижка
    elif category_upper == "STUDENT":
        return price * 0.9  # 10% знижка
    else:
        return price  # Без знижки


def calculate_bulk_discount(price, quantity):
    """
    Нараховує знижку за кількість товару.

    Args:
        price (float): Ціна одного товару
        quantity (int): Кількість товарів

    Returns:
        float: Загальна вартість зі знижкою

    Raises:
        ValueError: Якщо ціна або кількість від'ємні
        TypeError: Якщо параметри не є числами

    Знижки за кількість:
        - 10-49 шт: 5% знижка
        - 50-99 шт: 10% знижка
        - 100+ шт: 15% знижка
    """
    # Перевірка типів
    if not isinstance(price, (int, float)):
        raise TypeError("Ціна повинна бути числом")
    if not isinstance(quantity, int):
        raise TypeError("Кількість повинна бути цілим числом")

    # Перевірка на від'ємні значення
    if price < 0:
        raise ValueError("Ціна не може бути від'ємною")
    if quantity < 1:
        raise ValueError("Кількість не може бути менше одного")

    # Розраховуємо загальну вартість без знижки
    total = price * quantity

    # Застосовуємо знижку залежно від кількості
    if quantity >= 100:
        return total * 0.85  # 15% знижка
    elif quantity >= 50:
        return total * 0.90  # 10% знижка
    elif quantity >= 10:
        return total * 0.95  # 5% знижка
    else:
        return total  # Без знижки


if __name__ == "__main__":
    database = db.load_database()
    bayer_id = "abc"
    # create_balance = create_account(bayer_id, database, 100)
    # print(create_balance)
    balance_get = get_balance(bayer_id, database)
    print(balance_get)
    # new_depo = deposit(bayer_id, database, 100)
    # print(new_depo)
    # new_wth = withdraw(bayer_id, database, 100)
    # print(new_wth)
