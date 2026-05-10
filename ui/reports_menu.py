from models.reports import get_financial_report, get_equipment_status_report

def menu_reports():
    while True:
        print("\n=== Аналитика и отчетность ===")
        print("1. Финансовый отчет (Выручка и штрафы)")
        print("2. Отчет по состоянию фонда оборудования")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            # Используем корректное имя функции из models/reports.py
            data = get_financial_report() 
            print("\n" + "="*35)
            print("      ФИНАНСОВЫЙ ИТОГ      ")
            print("="*35)
            print(f"Доход от аренды:     {data['revenue']:>10.2f} руб.")
            print(f"Начислено штрафов:   {data['penalties']:>10.2f} руб.")
            print("-" * 35)
            total = data['revenue'] + data['penalties']
            print(f"ОБЩАЯ ВЫРУЧКА:       {total:>10.2f} руб.")
            print("="*35)
            
        elif choice == "2":
            # Группировка оборудования по статусам согласно анализу предметной области
            stats = get_equipment_status_report()
            print("\n--- Текущая дислокация активов ---")
            if not stats:
                print("Справочник оборудования пуст.")
            else:
                for status, count in stats:
                    print(f"Статус «{status}»: {count} ед.")
            print("-" * 35)
                
        elif choice == "0":
            break
        else:
            print("❌ Ошибка: выберите пункт от 0 до 2.")