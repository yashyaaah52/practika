"""Главный модуль приложения."""
import sys
from ui.menu_equipment import menu_equipment
from ui.client_menu import menu_clients
from ui.rental_menu import menu_rentals
from ui.booking_menu import menu_bookings
from ui.reports_menu import menu_reports
from ui.employee_menu import menu_employees
from database.db_manager import initialize_db


def show_main_menu():
    print("\n" + "="*40)
    print("   ИС УЧЕТА АРЕНДЫ ОБОРУДОВАНИЯ   ")
    print("="*40)
    print("1. Каталог оборудования")
    print("2. Управление клиентами")
    print("3. Оформление аренды / Возврат")
    print("4. Бронирование")
    print("5. Аналитика и отчеты")
    print("6. Управление персоналом")
    print("0. Завершить работу")
    print("="*40)
    return input("Выберите пункт меню: ")


def main():

    initialize_db()

    while True:
        choice = show_main_menu()

        if choice == "1":
            menu_equipment()
        elif choice == "2":
            menu_clients()
        elif choice == "3":
            menu_rentals()
        elif choice == "4":
            menu_bookings()
        elif choice == "5":
            menu_reports()
        elif choice == "6":
            menu_employees()
        elif choice == "0":
            print("Завершение сеанса... До свидания!")
            sys.exit()
        else:
            print("❌ Ошибка: Выберите корректный пункт меню (0-6).")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма принудительно остановлена.")
        sys.exit()
