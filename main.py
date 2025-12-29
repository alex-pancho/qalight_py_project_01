"""
Головний модуль консольного додатку для роздрібної мережі.
Забезпечує інтерфейс користувача та обробку команд.
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
    
import retail as rs
import database as db

database = db.load_database()


def print_menu():
    """Виводить головне меню програми."""
    print("\n" + "=" * 50)
    print("🏪 СИСТЕМА ОБЛІКУ РОЗДРІБНОЇ МЕРЕЖІ")
    print("=" * 50)
    print("1. Створити новий рахунок")
    print("2. Переглянути баланс")
    print("3. Поповнити рахунок")
    print("4. Зняти кошти")
    print("5. Інформація про рахунок")
    print("6. Список всіх рахунків")
    print("7. Калькулятор знижок")
    print("8. Калькулятор оптової знижки")
    print("9. Закрити рахунок")
    print("10. Резервна копія бази даних")
    print("0. Вихід")
    print("=" * 50)


def create_account_menu():
    """Меню створення нового рахунку."""
    print("\n📝 Створення нового рахунку")
    print("-" * 40)

    try:
        buyer_id = input("Введіть ID покупця: ").strip()

        balance_input = input("Початковий баланс (Enter для 0): ").strip()
        initial_balance = float(balance_input) if balance_input else 0.0

        # Завантажуємо базу даних
       

        # Викликаємо create_account з database як параметром
        balance = rs.create_account(buyer_id, database, initial_balance)

        print("\n✅ Рахунок успішно створено!")
        print(f"   ID: {buyer_id}")
        print(f"   Баланс: {balance:.2f} грн")

    except ValueError as e:
        print(f"\n❌ Помилка: {e}")
    except Exception as e:
        print(f"\n❌ Несподівана помилка: {e}")


def view_balance_menu():
    """Меню перегляду балансу."""
    print("\n💰 Перегляд балансу")
    print("-" * 40)

    try:
        bayer_id = input("Введіть ID покупця: ").strip()
        balance = rs.get_balance(bayer_id)
        print(f"\n✅ Баланс рахунку '{bayer_id}': {balance:.2f} грн")

    except ValueError as e:
        print(f"\n❌ Помилка: {e}")


def deposit_menu():
    """Меню поповнення рахунку."""
    print("\n➕ Поповнення рахунку")
    print("-" * 40)

    try:
        bayer_id = input("Введіть ID покупця: ").strip()
        amount = float(input("Сума поповнення (грн): "))

        new_balance = rs.deposit(bayer_id, database, amount)

    except ValueError as e:
        print(f"\n❌ Помилка: {e}")
    except Exception as e:
        print(f"\n❌ Несподівана помилка: {e}")


def withdraw_menu():
    """Меню зняття коштів."""
    print("\n➖ Зняття коштів")
    print("-" * 40)

    try:
        bayer_id = input("Введіть ID покупця: ").strip()
        amount = float(input("Сума зняття (грн): "))

        new_balance = rs.withdraw(bayer_id, database, amount)

    except ValueError as e:
        print(f"\n❌ Помилка: {e}")


def account_info_menu():
    """Меню перегляду повної інформації про рахунок."""
    print("\n📊 Інформація про рахунок")
    print("-" * 40)

    try:
        bayer_id = input("Введіть ID покупця: ").strip()

        # Отримуємо дані вручну, оскільки get_account_info може не існувати
        database = db.load_database()

        if bayer_id not in database:
            raise ValueError(f"Рахунок '{bayer_id}' не знайдено")

        account = database[bayer_id]

        print(f"\n{'='*40}")
        print(f"ID покупця: {account['bayer_id']}")
        print(f"Баланс: {account['balance']:.2f} грн")
        print(f"Категорія: {account.get('category', 'Regular')}")
        print(f"Кількість транзакцій: {len(account['transaction_history'])}")

        if account["transaction_history"]:
            print(f"\n📜 Остання транзакція:")
            last = account["transaction_history"][-1]
            print(f"   Тип: {last['type']}")
            print(f"   Сума: {last['amount']:.2f} грн")
            print(f"   Баланс після: {last['balance_after']:.2f} грн")

        print(f"{'='*40}")

    except ValueError as e:
        print(f"\n❌ Помилка: {e}")


def list_accounts_menu():
    """Меню перегляду всіх рахунків."""
    print("\n📋 Список всіх рахунків")
    print("-" * 40)

    accounts = db.load_database()

    if not accounts:
        print("\n⚠️  База даних порожня. Немає жодного рахунку.")
        return

    print(f"\nВсього рахунків: {len(accounts)}\n")

    for bayer_id, account in accounts.items():
        print(f"┌─ {bayer_id}")
        print(f"│  Баланс: {account['balance']:.2f} грн")
        print(f"│  Категорія: {account.get('category', 'Regular')}")
        print(f"└─ Транзакцій: {len(account['transaction_history'])}\n")


def discount_calculator_menu():
    """Калькулятор знижок за категорією."""
    print("\n🏷️  Калькулятор знижок за категорією")
    print("-" * 40)

    try:
        price = float(input("Ціна товару (грн): "))
        print("\nКатегорії: VIP (20%), Student (10%), Regular (0%)")
        category = input("Категорія клієнта: ").strip()

        final_price = rs.calculate_discount(price, category)
        discount_amount = price - final_price

        print(f"\n{'='*40}")
        print(f"Початкова ціна: {price:.2f} грн")
        print(f"Знижка: {discount_amount:.2f} грн")
        print(f"Фінальна ціна: {final_price:.2f} грн")
        print(f"{'='*40}")

    except (ValueError, TypeError) as e:
        print(f"\n❌ Помилка: {e}")


def bulk_discount_calculator_menu():
    """Калькулятор оптових знижок."""
    print("\n📦 Калькулятор оптових знижок")
    print("-" * 40)
    print("Знижки: 10-49 шт (5%), 50-99 шт (10%), 100+ шт (15%)")
    print()

    try:
        price = float(input("Ціна одного товару (грн): "))
        quantity = int(input("Кількість товарів: "))

        final_price = rs.calculate_bulk_discount(price, quantity)
        total_without_discount = price * quantity
        discount_amount = total_without_discount - final_price

        print(f"\n{'='*40}")
        print(f"Ціна за одиницю: {price:.2f} грн")
        print(f"Кількість: {quantity} шт")
        print(f"Сума без знижки: {total_without_discount:.2f} грн")
        print(f"Знижка: {discount_amount:.2f} грн")
        print(f"Фінальна сума: {final_price:.2f} грн")
        print(f"{'='*40}")

    except (ValueError, TypeError) as e:
        print(f"\n❌ Помилка: {e}")


def close_account_menu():
    """Меню закриття рахунку."""
    print("\n🗑️  Закриття рахунку")
    print("-" * 40)

    try:
        bayer_id = input("Введіть ID покупця: ").strip()

        # Показуємо інформацію перед закриттям
        database = db.load_database()
        if bayer_id not in database:
            raise ValueError(f"Рахунок '{bayer_id}' не знайдено")

        account = database[bayer_id]
        print(f"\nРахунок: {bayer_id}")
        print(f"Баланс: {account['balance']:.2f} грн")

        confirm = input("\n⚠️  Ви впевнені? (так/ні): ").strip().lower()

        if confirm in ["так", "yes", "y", "т"]:
            rs.close_account(bayer_id)
        else:
            print("\n❌ Операцію скасовано")

    except ValueError as e:
        print(f"\n❌ Помилка: {e}")


def backup_menu():
    """Меню створення резервної копії."""
    print("\n💾 Резервна копія бази даних")
    print("-" * 40)

    try:
        db.backup_database()
    except Exception as e:
        print(f"\n❌ Помилка створення резервної копії: {e}")


def main():
    """Головна функція програми."""
    print("\n" + "🎉 Вітаємо у системі обліку роздрібної мережі! 🎉".center(50))

    while True:
        print_menu()

        try:
            choice = input("\n👉 Оберіть опцію (0-10): ").strip()

            if choice == "1":
                create_account_menu()
            elif choice == "2":
                view_balance_menu()
            elif choice == "3":
                deposit_menu()
            elif choice == "4":
                withdraw_menu()
            elif choice == "5":
                account_info_menu()
            elif choice == "6":
                list_accounts_menu()
            elif choice == "7":
                discount_calculator_menu()
            elif choice == "8":
                bulk_discount_calculator_menu()
            elif choice == "9":
                close_account_menu()
            elif choice == "10":
                backup_menu()
            elif choice == "0":
                print("\n👋 Дякуємо за використання системи! До побачення!")
                break
            else:
                print("\n❌ Невірний вибір. Спробуйте ще раз.")

        except KeyboardInterrupt:
            print("\n\n👋 Програму зупинено користувачем.")
            break
        except Exception as e:
            print(f"\n❌ Несподівана помилка: {e}")
            print("Спробуйте ще раз або зверніться до адміністратора.")


if __name__ == "__main__":
    main()
