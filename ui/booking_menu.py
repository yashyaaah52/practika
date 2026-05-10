from database.db_manager import get_connection

class Booking:
    def __init__(self, booking_id=None, client_id=None, equipment_id=None, 
                 start_date=None, end_date=None, status="Ожидание"):
        self.id = booking_id
        self.client_id = client_id
        self.equipment_id = equipment_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def save(self):
        """Сохраняет новую бронь или обновляет существующую [cite: 90, 94]"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO Bookings (ClientID, EquipmentID, StartDate, EndDate, Status)
                VALUES (?, ?, ?, ?, ?)
            """, (self.client_id, self.equipment_id, self.start_date, self.end_date, self.status))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE Bookings SET ClientID = ?, EquipmentID = ?, StartDate = ?, EndDate = ?, Status = ?
                WHERE BookingID = ?
            """, (self.client_id, self.equipment_id, self.start_date, self.end_date, self.status, self.id))
        conn.commit()
        conn.close()

def check_availability(equipment_id, start_date, end_date):
    """
    Проверка доступности оборудования на указанные даты[cite: 72, 73, 74].
    Возвращает True, если пересечений с другими бронями нет.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Логика поиска пересекающихся интервалов дат [cite: 83]
    cursor.execute("""
        SELECT COUNT(*) FROM Bookings 
        WHERE EquipmentID = ? AND Status != 'Отменена'
        AND NOT (EndDate < ? OR StartDate > ?)
    """, (equipment_id, start_date, end_date))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0