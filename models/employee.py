from database.db_manager import get_connection

class Employee:
    def __init__(self, employee_id=None, name=None, position=None, phone=None):
        self.id = employee_id
        self.name = name
        self.position = position
        self.phone = phone

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO Employees (name, position, phoneNumber) VALUES (?, ?, ?)
            """, (self.name, self.position, self.phone))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE Employees SET name = ?, position = ?, phoneNumber = ? WHERE EmployeeID = ?
            """, (self.name, self.position, self.phone, self.id))
        conn.commit()
        conn.close()

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT EmployeeID, name, position, phoneNumber FROM Employees")
    rows = cursor.fetchall()
    conn.close()
    return [Employee(*row) for row in rows]