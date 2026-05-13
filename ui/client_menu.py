from models.client import Client, get_client_by_id, get_all_client


def menu_clients():
    while True:
        print("\n=== Управление клиентами ===")
        print("1. Список всех клиентов")
        print("2. Регистрация нового клиента")
        print("3. Изменить данные/статус благонадежности")
        print("4. Удалить клиента")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            clients = get_all_client()
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
            id_to_edit = int(input("Введите ID клиента для редактирования: "))
            current_client = get_client_by_id(id_to_edit)
            
            if not current_client:
                print("❌ Клиент с таким ID не найден!")
                continue

            print("\nОставьте поле пустым, чтобы не изменять текущее значение")
            name = input(f"Новое ФИО [{current_client.name}]: ")
            passport = input(f"Новые паспортные данные [{current_client.passport}]: ")
            phone = input(f"Новый номер телефона [{current_client.phone}]: ")
            reliability = input(f"Новый статус благонадежности [{current_client.reliability}]: ")

            updated_client = Client(
                client_id=id_to_edit,
                name=name if name else current_client.name,
                passport=passport if passport else current_client.passport,
                phone=phone if phone else current_client.phone,
                reliability=reliability if reliability else current_client.reliability,
            )
            updated_client.save()
            print("🔄 Данные клиента обновлены.")
        
        elif choice == "4":
            id_to_delete = input("Введите ID клиента для удаления: ")
            client = Client(client_id=int(id_to_delete))
            client.delete()
            print("🗑️ Запись удалена.")

        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод.")