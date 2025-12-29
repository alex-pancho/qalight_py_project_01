"""Модуль для роботи з JSON базою даних.
Забезпечує завантаження та збереження даних про рахунки покупців.
"""
import json
from pathlib import Path


project_path = Path(__file__).parent
DB_PATH = project_path / "data" / "accounts.json"

def load_database(db_path=DB_PATH):
    """
    Docstring for load_database
    
    :param db_path: Description
    """
    try:
        with open(db_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"❌ Помилка читання бази даних: {e}")
        print("⚠️  Повертаємо порожню базу даних")
        # Повертаємо порожню базу у випадку помилки
        return {}
    except FileNotFoundError:
        print(f"⚠️  Файл бази даних не знайдено, створюємо новий")
        #ensure_database_exists()
        return {}


def save_database(database, db_path=DB_PATH):
    """
    Docstring for save_database
    
    :param database: Description
    """
    try:
        with open(db_path, "w", encoding="utf-8") as file:
            # indent=2 робить JSON читабельним з відступами
            # ensure_ascii=False дозволяє зберігати українські символи
            json.dump(database, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Помилка збереження бази даних: {e}")
        raise


def count_accounts(db_path=DB_PATH):
    """
    Docstring for count_accounts
    """
    database = load_database(db_path)
    return len(database)


def ensure_database_exists():
    """
    Створює файл бази даних та папку, якщо їх немає.

    Ця функція викликається автоматично при імпорті модуля.
    """
    # Створюємо папку data, якщо її немає
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Якщо файлу немає, створюємо порожню базу
    if not DB_PATH.exists():
        with open(DB_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False, indent=2)
        print(f"✓ Створено нову базу даних: {DB_PATH}")
    else:
        """
        if size_bytes < 1024 * 1024:
            size = size_bytes / 1024
            unit = "kB"
        else:
            size = size_bytes / 1024 / 1024
            unit = "MB"

        print(
            f"База уже існує за вказаним шляхом:\n"
            f"{DB_PATH}\n"
            f"{size:.2f} {unit}"
        )
        """
        size_bytes = DB_PATH.stat().st_size
        size = size_bytes / 1024 / 1024
        unit = "MB"
        if size < 1:
            size = size_bytes / 1024
            unit = "KB"
        print("База уже існує за вказаним шляхом:\n" f"{DB_PATH}\n{size:.2f} {unit}")


def backup_database():
    """
    Створює резервну копію бази даних.

    Копія зберігається в файл з розширенням .backup
    Наприклад: accounts.json.backup
    """
    if DB_PATH.exists():
        backup_path = DB_PATH.with_suffix(".json.backup")
        try:
            database = load_database()
            with open(backup_path, "w", encoding="utf-8") as file:
                json.dump(database, file, ensure_ascii=False, indent=2)
            print(f"✓ Створено резервну копію: {backup_path}")
        except Exception as e:
            print(f"❌ Помилка створення резервної копії: {e}")


def get_database_path():
    """
    Повертає шлях до файлу бази даних.

    Returns:
        Path: Об'єкт Path з шляхом до бази даних
    """
    return DB_PATH
