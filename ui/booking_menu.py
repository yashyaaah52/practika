from datetime import datetime

from models.booking import (
    Booking,
    check_availability,
    get_all_bookings
)

from models.client import get_all_client
from models.equipment import get_all_equipment


def menu_bookings():

    while True:

        print("\n" + "=" * 30)
        print("   МЕНЮ БРОНИРОВАНИЯ")
        print("=" * 30)

        print("1. Проверить доступность и создать бронь")
        print("2. Просмотреть все брони")
        print("3. Удалить бронь")
        print("0. Назад в главное меню")

        print("=" * 30)

        choice = input("Выберите действие: ")

        # Создание брони
        if choice == "1":

            print("\n--- Выбор оборудования ---")

            items = get_all_equipment()

            for i in items:
                print(
                    f"ID: {i.id} | "
                    f"{i.name} "
                    f"(Статус: {i.status})"
                )

            eq_id = int(input("\nВведите ID оборудования: "))

            # Проверка дат
            while True:

                start_date = input(
                    "Дата начала (ГГГГ-ММ-ДД): "
                )

                end_date = input(
                    "Дата окончания (ГГГГ-ММ-ДД): "
                )

                try:

                    datetime.strptime(
                        start_date,
                        "%Y-%m-%d"
                    )

                    datetime.strptime(
                        end_date,
                        "%Y-%m-%d"
                    )

                    # Проверка порядка дат
                    if end_date < start_date:

                        print(
                            "\n❌ Дата окончания "
                            "не может быть раньше "
                            "даты начала."
                        )

                        continue

                    break

                except ValueError:

                    print(
                        "\n❌ Неверный формат даты.\n"
                        "Используйте формат: ГГГГ-ММ-ДД"
                    )

            # Проверка доступности
            if check_availability(
                eq_id,
                start_date,
                end_date
            ):

                print("\n--- Выбор клиента ---")

                clients = get_all_client()

                for c in clients:
                    print(
                        f"ID: {c.id} | {c.name}"
                    )

                cl_id = int(
                    input("\nВведите ID клиента: ")
                )

                # Создание брони
                new_booking = Booking(
                    client_id=cl_id,
                    equipment_id=eq_id,
                    start_date=start_date,
                    end_date=end_date,
                    status="Ожидание"
                )

                new_booking.save()

                print(
                    "\n✅ Бронирование успешно создано!"
                )

            else:

                print(
                    "\n❌ Оборудование занято "
                    "на выбранные даты."
                )

        # Просмотр броней
        elif choice == "2":

            bookings = get_all_bookings()

            print("\n--- СПИСОК БРОНЕЙ ---")

            if len(bookings) == 0:

                print("Броней нет.")

            else:

                for b in bookings:

                    print(
                        f"ID брони: {b[0]} | "
                        f"Клиент: {b[1]} | "
                        f"Оборудование: {b[2]} | "
                        f"С {b[3]} по {b[4]} | "
                        f"Статус: {b[5]}"
                    )

        elif choice == "3":
            id_to_delete = input("Введите ID брони для удаления: ")
            booking = Booking(booking_id=int(id_to_delete))
            booking.delete()
            print("🗑️ Запись удалена.")

        elif choice == "0":
            break

        else:
            print("\n❌ Неверный ввод.")