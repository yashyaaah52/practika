import sqlite3

# Импорт имени файла 
from config import DB_NAME 

# Функция для подключения к базе данных
def get_connection():
    return sqlite3.connect(DB_NAME)

# Функция инициализации базы данных: создаёт все таблицы из физической модели
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Создание таблицы "Клиенты"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Client (
        ClientID INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор
        FullName TEXT NOT NULL,                     -- ФИО клиента
        PassportData TEXT,                          -- Паспортные данные
        Phone TEXT,                                 -- Номер телефона
        Reliability TEXT                            -- Статус благонадежности
    )
    ''')

    # Создание таблицы "Сотрудники" 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор
        Phone TEXT,                                   -- Номер телефона
        FullName TEXT NOT NULL,                       -- ФИО сотрудника
        Passport TEXT                                 -- Паспортные данные
    )
    ''')

    # Создание таблицы "Оборудование" 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Equipment (
        EquipmentID INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор
        name TEXT NOT NULL,                            -- Название оборудования
        category TEXT,                                 -- Категория
        serialnumber TEXT,                             -- Серийный/инвентарный номер
        dailyCost REAL NOT NULL,                       -- Стоимость за сутки
        status TEXT,                                   -- Статус (на складе, в аренде и т.д.)
        condition TEXT                                 -- Состояние оборудования
    )
    ''')

    # Создание таблицы "Бронь"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Bookings (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT, -- Уникальный идентификатор
        ClientID INTEGER,                            -- Внешний ключ: ID клиента
        EquipmentID INTEGER,                         -- Внешний ключ: ID оборудования
        StartDate TEXT,                              -- Дата начала брони (храним как строку ISO 8601)
        EndDate TEXT,                                -- Дата окончания брони
        Status TEXT,                                 -- Статус бронирования
        FOREIGN KEY (ClientID) REFERENCES Client(ClientID),
        FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
    )
    ''')

    # Создание таблицы "Аренда"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Rentals (
        RentalID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный идентификатор
        ClientID INTEGER,                            -- Внешний ключ: ID клиента
        EmployeeID INTEGER,                          -- Внешний ключ: ID сотрудника, оформившего аренду
        EquipmentID INTEGER,                         -- Внешний ключ: ID оборудования
        IssueDate TEXT,                              -- Дата выдачи
        PlannedReturn TEXT,                          -- Плановая дата возврата
        ActualReturn TEXT,                           -- Фактическая дата возврата
        TotalCost REAL,                              -- Итоговая стоимость
        penaltyAmount REAL,                          -- Сумма штрафа
        Status TEXT,                                 -- Статус сделки
        FOREIGN KEY (ClientID) REFERENCES Client(ClientID),
        FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
        FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID)
    )
    ''')

    # Сохраняем изменения
    conn.commit()
    # Закрываем соединение с базой данных
    conn.close()

# Блок для проверки запуска (создаст БД при прямом запуске файла)
if __name__ == "__main__":
    initialize_db()
    print("База данных успешно инициализирована.")