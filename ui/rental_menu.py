"""Модуль работы с арендой."""
from datetime import datetime

from models.rental import Rental, get_all_rentals, get_rental_by_id
from models.client import get_all_client
from models.equipment import get_all_equipment, get_equipment_by_id
from models.employee import get_all_employees


def calculate_rental_cost(equipment_id, start_date_str, end_date_str):
    """Вспомогательная функция для расчета стоимости: ставка * дни"""

    try:
        equipment = get_equipment_by_id(equipment_id)

        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.strptime(end_date_str, "%Y-%m-%d")

        days = (end - start).days

        if days <= 0:
            days = 1

        return days * equipment.daily_cost

    except Exception:
        return 0.0


def menu_rentals():

    while True:

        print("\n=== Управление Арендой ===")
        print("1. Показать все договоры аренды")
        print("2. Оформить новую аренду")
        print("3. Удалить запись об аренде")
        print("4. Оформить возврат оборудования")
        print("0. Назад в главное меню")

        choice = input("Выберите действие: ")

        if choice == "1":

            rentals = get_all_rentals()

            print("\nСписок договоров аренды:")

            for r in rentals:

                print(
                    f"ID: {r[0]} | Клиент: {r[1]} | "
                    f"Сотрудник: {r[2]} | Оборудование: {r[3]} | "
                    f"Выдача: {r[4]} | План возврата: {r[5]} | "
                    f"Сумма: {r[7]} руб. | Статус: {r[9]}"
                )

        elif choice == "2":

            print("\n=== Оформление нового договора ===")

            # 1. Выбор клиента
            clients = get_all_client()

            for c in clients:
                print(f"{c.id}. {c.name}")

            client_id = int(input("Введите ID клиента: "))

            # 2. Выбор оборудования
            equipment_list = get_all_equipment()

            for e in equipment_list:

                if e.status == "На складе":
                    print(f"{e.id}. {e.name} ({e.daily_cost} руб/сут)")

            equipment_id = int(input("Введите ID оборудования: "))

            # 3. Выбор сотрудника
            employees = get_all_employees()

            for emp in employees:
                print(f"{emp.id}. {emp.name}")

            employee_id = int(input("Введите ID сотрудника: "))

            # 4. Даты
            issue_date = datetime.now().strftime("%Y-%m-%d")

            print(f"Дата выдачи (сегодня): {issue_date}")

            while True:

                planned_return = input("Введите дату возврата (ГГГГ-ММ-ДД): ")

                try:

                    datetime.strptime(planned_return, "%Y-%m-%d")

                    if planned_return < issue_date:
                        print("❌ Дата возврата раньше даты выдачи.")
                        continue

                    break

                except Exception:
                    print("❌ Неверный формат даты.")

            # Расчет стоимости
            total = calculate_rental_cost(
                equipment_id,
                issue_date,
                planned_return
            )

            rental = Rental(
                client_id=client_id,
                employee_id=employee_id,
                equipment_id=equipment_id,
                issue_date=issue_date,
                planned_return=planned_return,
                total_cost=total,
                status="Активна"
            )

            rental.save()

            print(f"✅ Аренда оформлена. Итоговая стоимость: {total:.2f} руб.")

        elif choice == "3":

            id_to_delete = input("Введите ID аренды для удаления: ")

            rental = Rental(rental_id=int(id_to_delete))

            rental.delete()

            print("🗑️ Запись удалена.")

        elif choice == "4":

            rental_id = int(
                input("Введите ID аренды для оформления возврата: "))

            rental = get_rental_by_id(rental_id)

            if rental:

                actual_return = datetime.now().strftime("%Y-%m-%d")

                rental.actual_return = actual_return
                rental.status = "Завершена"

                # Пересчет стоимости
                rental.total_cost = calculate_rental_cost(
                    rental.equipment_id,
                    rental.issue_date,
                    actual_return
                )

                # Штраф за просрочку
                planned = datetime.strptime(rental.planned_return, "%Y-%m-%d")
                actual = datetime.strptime(actual_return, "%Y-%m-%d")

                if actual > planned:

                    overdue_days = (actual - planned).days

                    equipment = get_equipment_by_id(rental.equipment_id)

                    rental.penalty_amount = overdue_days * \
                        (equipment.daily_cost * 1.5)

                    print(f"⚠️ Просрочка {overdue_days} дн. "
                          f"Штраф: {rental.penalty_amount} руб.")

                rental.save()

                print(f"✅ Оборудование возвращено {actual_return}. "
                      f"Итоговая сумма: "
                      f"{rental.total_cost + rental.penalty_amount:.2f} руб.")

            else:
                print("❌ Договор не найден.")

        elif choice == "0":
            break

        else:
            print("❌ Неверный ввод.")
