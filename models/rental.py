from database.db_manager import get_connection


class Rental:
    def __init__(self, rental_id=None, client_id=None, employee_id=None,
                 equipment_id=None, issue_date=None, planned_return=None,
                 actual_return=None, total_cost=0.0,
                 penalty_amount=0.0, status=None):

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

        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:

            cursor.execute("""
                INSERT INTO Rentals (
                    ClientID, EmployeeID, EquipmentID,
                    IssueDate, PlannedReturn, ActualReturn,
                    TotalCost, penaltyAmount, Status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.client_id, self.employee_id,
                self.equipment_id, self.issue_date,
                self.planned_return, self.actual_return,
                self.total_cost, self.penalty_amount,
                self.status
            ))

            self.id = cursor.lastrowid

        else:

            cursor.execute("""
                UPDATE Rentals SET
                    ClientID = ?, EmployeeID = ?,
                    EquipmentID = ?, IssueDate = ?,
                    PlannedReturn = ?, ActualReturn = ?,
                    TotalCost = ?, penaltyAmount = ?,
                    Status = ?
                WHERE RentalID = ?
            """, (
                self.client_id, self.employee_id,
                self.equipment_id, self.issue_date,
                self.planned_return, self.actual_return,
                self.total_cost, self.penalty_amount,
                self.status, self.id
            ))

        conn.commit()
        conn.close()

    def delete(self):

        if self.id:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM Rentals WHERE RentalID = ?",
                (self.id,)
            )

            conn.commit()
            conn.close()


def get_all_rentals():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.RentalID, c.Fullname,
            emp.FullName, e.name,
            r.IssueDate, r.PlannedReturn,
            r.ActualReturn, r.TotalCost,
            r.penaltyAmount, r.Status
        FROM Rentals r
        JOIN Client c ON r.ClientID = c.ClientID
        JOIN Employees emp ON r.EmployeeID = emp.EmployeeID
        JOIN Equipment e ON r.EquipmentID = e.EquipmentID
    """)

    rentals = cursor.fetchall()

    conn.close()

    return rentals


def get_rental_by_id(rental_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT RentalID, ClientID, EmployeeID,
               EquipmentID, IssueDate,
               PlannedReturn, ActualReturn,
               TotalCost, penaltyAmount, Status
        FROM Rentals
        WHERE RentalID = ?
    """, (rental_id,))

    row = cursor.fetchone()

    conn.close()

    if row:

        return Rental(
            rental_id=row[0], client_id=row[1], employee_id=row[2], equipment_id=row[3],
            issue_date=row[4], planned_return=row[5], actual_return=row[6], total_cost=row[7],
            penalty_amount=row[8], status=row[9])

    return None