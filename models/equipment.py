"""Модуль работы с обордованием."""
from database.db_manager import get_connection


class Equipment:
    """Класс оборудование."""
    def __init__(self, equipment_id=None, name=None, category=None,
                 serial_number=None, daily_cost=None, status=None, condition=None):
        self.id = equipment_id
        self.name = name
        self.category = category
        self.serial_number = serial_number
        self.daily_cost = daily_cost
        self.status = status
        self.condition = condition

    def save(self):
        """Добавляет новое оборудование или обновляет существующее"""
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            # Создание новой записи
            cursor.execute("""
                INSERT INTO Equipment (name, category, serialnumber, dailyCost, status, condition)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.name, self.category, self.serial_number,
                  self.daily_cost, self.status, self.condition))
            self.id = cursor.lastrowid
        else:
            # Обновление существующей записи
            cursor.execute("""
                UPDATE Equipment
                SET name = ?, category = ?, serialnumber = ?, dailyCost = ?, status = ?, condition = ?
                WHERE EquipmentID = ?
            """, (self.name, self.category, self.serial_number,
                  self.daily_cost, self.status, self.condition, self.id))

        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет оборудование из базы данных"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Equipment WHERE EquipmentID = ?", (self.id,))
            conn.commit()
            conn.close()

# Вспомогательные функции для выборки данных


def get_all_equipment():
    """Возвращает список всех единиц оборудования"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EquipmentID, name, category, serialnumber, dailyCost, status, condition
        FROM Equipment
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        Equipment(
            equipment_id=row[0], name=row[1], category=row[2],
            serial_number=row[3], daily_cost=row[4], status=row[5], condition=row[6]
        )
        for row in rows
    ]


def get_equipment_by_id(equipment_id):
    """Находит конкретное оборудование по его ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EquipmentID, name, category, serialnumber, dailyCost, status, condition
        FROM Equipment
        WHERE EquipmentID = ?
    """, (equipment_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Equipment(
            equipment_id=row[0], name=row[1], category=row[2],
            serial_number=row[3], daily_cost=row[4], status=row[5], condition=row[6]
        )
    return None
