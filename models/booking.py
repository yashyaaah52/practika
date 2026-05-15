"""Модуль работы с арендой."""
from database.db_manager import get_connection


class Booking:
    """Класс бронь."""
    def __init__(self, booking_id=None, client_id=None, equipment_id=None,
                 start_date=None, end_date=None, status="Ожидание"):

        self.id = booking_id
        self.client_id = client_id
        self.equipment_id = equipment_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        # Создание новой брони
        if self.id is None:
            cursor.execute("""
                INSERT INTO Bookings
                (ClientID, EquipmentID, StartDate, EndDate, Status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.client_id,
                self.equipment_id,
                self.start_date,
                self.end_date,
                self.status
            ))

            self.id = cursor.lastrowid

        # Обновление существующей брони
        else:
            cursor.execute("""
                UPDATE Bookings
                SET ClientID = ?,
                    EquipmentID = ?,
                    StartDate = ?,
                    EndDate = ?,
                    Status = ?
                WHERE BookingID = ?
            """, (
                self.client_id,
                self.equipment_id,
                self.start_date,
                self.end_date,
                self.status,
                self.id
            ))

        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет бронь из базы данных"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM Booking WHERE BookingID = ?", (self.id,))
            conn.commit()
            conn.close()


# Проверка доступности оборудования
def check_availability(equipment_id, start_date, end_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Bookings
        WHERE EquipmentID = ?
        AND Status != 'Отменена'
        AND (
            (StartDate <= ? AND EndDate >= ?)
            OR
            (StartDate <= ? AND EndDate >= ?)
        )
    """, (
        equipment_id,
        end_date,
        end_date,
        start_date,
        start_date
    ))

    count = cursor.fetchone()[0]

    conn.close()

    return count == 0


# Получение всех броней
def get_all_bookings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            b.BookingID, c.Fullname, e.name,
            b.StartDate, b.EndDate, b.Status
        FROM Bookings b
        JOIN Client c
            ON b.ClientID = c.ClientID
        JOIN Equipment e
            ON b.EquipmentID = e.EquipmentID
    """)

    bookings = cursor.fetchall()

    conn.close()

    return bookings
