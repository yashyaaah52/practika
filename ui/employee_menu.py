from models.employee import Employee, get_all_employees

def menu_employees():
    while True:
        print("\n=== Управление персоналом ===")
        print("1. Список сотрудников")
        print("2. Добавить сотрудника")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            employees = get_all_employees()
            for e in employees:
                print(f"ID: {e.id} | {e.name} — {e.position}")
        
        elif choice == "2":
            name = input("ФИО сотрудника: ")
            pos = input("Должность: ")
            phone = input("Телефон: ")
            emp = Employee(name=name, position=pos, phone=phone)
            emp.save()
            print("✅ Сотрудник добавлен.")
            
        elif choice == "0":
            break