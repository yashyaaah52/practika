from models.client import Client, get_all_clients

def menu_clients():
    while True:
        print("\n=== Управление клиентами ===")
        print("1. Список всех клиентов")
        print("2. Регистрация нового клиента")
        print("3. Изменить данные/статус благонадежности")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            clients = get_all_clients()
            print("\nБаза клиентов:")
            for c in clients:
                print(f"ID: {c.id} | {c.name} | Тел: {c.phone} | Статус: {c.reliability}")

        elif choice == "2":
            print("\n=== Регистрация клиента ===")
            name = input("ФИО: ")
            passport = input("Паспортные данные: ")
            phone = input("Номер телефона: ")
            # По умолчанию при регистрации ставим "Высокая"
            client = Client(name=name, passport=passport, phone=phone, reliability="Высокая")
            client.save()
            print("✅ Клиент успешно зарегистрирован.")

        elif choice == "3":
            client_id = int(input("Введите ID клиента для редактирования: "))
            # Логика поиска и изменения (аналогично оборудованию)
            # Здесь менеджер может вручную понизить статус, если клиент проблемный
            print("1. Изменить телефон")
            print("2. Изменить статус благонадежности")
            # ... и так далее
            
        elif choice == "0":
            break