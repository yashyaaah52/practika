from models.equipment import Equipment, get_all_equipment, get_equipment_by_id

def menu_equipment():
    while True:
        print("\n=== Управление оборудованием ===")
        print("1. Показать весь каталог")
        print("2. Добавить новое оборудование")
        print("3. Удалить оборудование")
        print("4. Редактировать данные оборудования")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            equipment_list = get_all_equipment()
            print("\nКаталог оборудования:")
            print("-" * 110)
            for item in equipment_list:
                print(f"ID: {item.id} | {item.name} [{item.category}] | "
                      f"S/N: {item.serial_number} | Цена/сутки: {item.daily_cost} руб. | "
                      f"Статус: {item.status} | Состояние: {item.condition}")
            print("-" * 110)

        elif choice == "2":
            print("\n=== Регистрация нового оборудования ===")
            name = input("Наименование: ")
            category = input("Категория (например, Электроинструмент): ")
            serial_number = input("Серийный номер: ")
            daily_cost = float(input("Стоимость аренды за сутки: "))
            status = input("Текущий статус (например, На складе): ")
            condition = input("Техническое состояние (например, Новое): ")
            
            new_item = Equipment(
                name=name,
                category=category,
                serial_number=serial_number,
                daily_cost=daily_cost,
                status=status,
                condition=condition
            )
            new_item.save()
            print("✅ Оборудование успешно внесено в базу.")

        elif choice == "3":
            id_to_delete = input("Введите ID оборудования для удаления: ")
            item = Equipment(equipment_id=int(id_to_delete))
            item.delete()
            print("🗑️ Запись удалена.")

        elif choice == "4":
            id_to_edit = int(input("Введите ID оборудования для редактирования: "))
            current_item = get_equipment_by_id(id_to_edit)
            
            if not current_item:
                print("❌ Оборудование с таким ID не найдено!")
                continue

            print("\nОставьте поле пустым, чтобы не изменять текущее значение")
            name = input(f"Новое название [{current_item.name}]: ")
            category = input(f"Новая категория [{current_item.category}]: ")
            serial_number = input(f"Новый серийный номер [{current_item.serial_number}]: ")
            daily_cost = input(f"Новая стоимость/сутки [{current_item.daily_cost}]: ")
            status = input(f"Новый статус [{current_item.status}]: ")
            condition = input(f"Новое состояние [{current_item.condition}]: ")

            updated_item = Equipment(
                equipment_id=id_to_edit,
                name=name if name else current_item.name,
                category=category if category else current_item.category,
                serial_number=serial_number if serial_number else current_item.serial_number,
                daily_cost=float(daily_cost) if daily_cost else current_item.daily_cost,
                status=status if status else current_item.status,
                condition=condition if condition else current_item.condition
            )
            updated_item.save()
            print("🔄 Данные оборудования обновлены.")

        elif choice == "0":
            break
        else:
            print("❌ Неверный ввод.")