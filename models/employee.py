"""Модуль работы с сотрудниками."""
from database.db_manager import get_connection


class Employee:
    """Класс сотрудник."""
    def __init__(self, employee_id=None, phone=None, name=None, passport=None):
        self.id = employee_id
        self.phone = phone
        self.name = name
        self.passport = passport

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            # Fixed: Column names matched to Employees schema
            cursor.execute("""
                INSERT INTO Employees (Phone, FullName, Passport) VALUES (?, ?, ?)
            """, (self.phone, self.name, self.passport))
            self.id = cursor.lastrowid
        else:
            # Fixed: Column names matched to Employees schema
            cursor.execute("""
                UPDATE Employees SET Phone = ?, FullName = ?, Passport = ? WHERE EmployeeID = ?
            """, (self.phone, self.name, self.passport, self.id))
        conn.commit()
        conn.close()


def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    # Fixed: Selected columns matched to Employees schema
    cursor.execute(
        "SELECT EmployeeID, Phone, FullName, Passport FROM Employees")
    rows = cursor.fetchall()
    conn.close()
    return [Employee(*row) for row in rows]
