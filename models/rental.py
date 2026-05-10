from database.db_manager import get_connection

class Rental:
    def __init__(self, rental_id=None, client_id=None, employee_id=None, 
                 equipment_id=None, issue_date=None, planned_return=None, 
                 actual_return=None, total_cost=0.0, penalty_amount=0.0, status=None):
        self.id = rental_id
        self.client_id = client_id
        self.employee_id = employee_id
        self.equipment_id = equipment_id
        self.issue_date = issue_date
        self.planned_return = planned_return
        self.actual_return = actual_return
        self.total_cost = total_cost
        self.penalty_amount = penalty_amount
        self.status = status

    def save(self):
        """Добавляет новую запись об аренде или обновляет существующую"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            # Создание новой записи об аренде
            cursor.execute("""
                INSERT INTO Rentals (
                    ClientID, EmployeeID, EquipmentID, IssueDate, 
                    PlannedReturn, ActualReturn, TotalCost, penaltyAmount, Status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.client_id, self.employee_id, self.equipment_id, self.issue_date,
                  self.planned_return, self.actual_return, self.total_cost, 
                  self.penalty_amount, self.status))
            self.id = cursor.lastrowid
        else:
            # Обновление существующей записи (например, при возврате оборудования)
            cursor.execute("""
                UPDATE Rentals SET 
                    ClientID = ?, EmployeeID = ?, EquipmentID = ?, IssueDate = ?, 
                    PlannedReturn = ?, ActualReturn = ?, TotalCost = ?, 
                    penaltyAmount = ?, Status = ?
                WHERE RentalID = ?
            """, (self.client_id, self.employee_id, self.equipment_id, self.issue_date,
                  self.planned_return, self.actual_return, self.total_cost, 
                  self.penalty_amount, self.status, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет запись об аренде"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Rentals WHERE RentalID = ?", (self.id,))
            conn.commit()
            conn.close()

# Вспомогательные функции

def get_all_rentals():
    """Возвращает список всех оформленных аренд"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RentalID, ClientID, EmployeeID, EquipmentID, IssueDate, 
               PlannedReturn, ActualReturn, TotalCost, penaltyAmount, Status 
        FROM Rentals
    """)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        Rental(
            rental_id=row[0], client_id=row[1], employee_id=row[2], 
            equipment_id=row[3], issue_date=row[4], planned_return=row[5], 
            actual_return=row[6], total_cost=row[7], penalty_amount=row[8], 
            status=row[9]
        ) for row in rows
    ]

def get_rental_by_id(rental_id):
    """Возвращает запись об аренде по её ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RentalID, ClientID, EmployeeID, EquipmentID, IssueDate, 
               PlannedReturn, ActualReturn, TotalCost, penaltyAmount, Status 
        FROM Rentals WHERE RentalID = ?
    """, (rental_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return Rental(
            rental_id=row[0], client_id=row[1], employee_id=row[2], 
            equipment_id=row[3], issue_date=row[4], planned_return=row[5], 
            actual_return=row[6], total_cost=row[7], penalty_amount=row[8], 
            status=row[9]
        )
    return None