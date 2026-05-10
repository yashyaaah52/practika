from models.booking import Booking, check_availability
from models.client import get_all_clients
from models.equipment import get_all_equipment

def menu_bookings():
    while True:
        print("\n" + "="*30)
        print("   МЕНЮ БРОНИРОВАНИЯ   ")
        print("="*30)
        print("1. Проверить доступность и создать бронь")
        print("2. Просмотреть все брони")
        print("0. Назад в главное меню")
        print("="*30)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            print("\n--- Выбор оборудования ---")
            items = get_all_equipment()
            for i in items:
                print(f"ID: {i.id} | {i.name} (Статус: {i.status})")
            
            eq_id = int(input("\nВведите ID оборудования: "))
            start_date = input("Дата начала (ГГГГ-ММ-ДД): ")
            end_date = input("Дата окончания (ГГГГ-ММ-ДД): ")
            
            # Проверка доступности через функцию из моделей
            if check_availability(eq_id, start_date, end_date):
                print("\n--- Выбор клиента ---")
                clients = get_all_clients()
                for c in clients:
                    print(f"ID: {c.id} | {c.name}")
                
                cl_id = int(input("\nВведите ID клиента: "))
                
                # Создание записи
                new_booking = Booking(
                    client_id=cl_id, 
                    equipment_id=eq_id, 
                    start_date=start_date, 
                    end_date=end_date,
                    status="Ожидание"
                )
                new_booking.save()
                print("\n✅ Бронирование успешно создано!")
            else:
                print("\n❌ Ошибка: Оборудование занято на выбранные даты.")
        
        elif choice == "2":
            # Здесь можно добавить вызов функции get_all_bookings, если она есть в моделях
            print("\nФункция просмотра списка броней в разработке...")
            
        elif choice == "0":
            break
        else:
            print("\n❌ Неверный ввод.")