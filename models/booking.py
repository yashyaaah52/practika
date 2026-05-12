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
    """Проверка: нет ли пересечений по датам для данного оборудования"""
    conn = get_connection()
    cursor = conn.cursor()
    # Проверяем пересечения с существующими бронями и активными арендами
    cursor.execute("""
        SELECT COUNT(*) FROM Bookings 
        WHERE EquipmentID = ? AND Status != 'Отменена'
        AND ((StartDate <= ? AND EndDate >= ?) OR (StartDate <= ? AND EndDate >= ?))
    """, (equipment_id, end_date, end_date, start_date, start_date))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

#функция для вывода всех броней
def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT BookingID, ClientID, EquipmentID,
               StartDate, EndDate, Status
        FROM Bookings
    """)

    rows = cursor.fetchall()

    bookings = []

    for row in rows:
        booking = Booking(
            booking_id=row[0],
            client_id=row[1],
            equipment_id=row[2],
            start_date=row[3],
            end_date=row[4],
            status=row[5]
        )

        bookings.append(booking)

    conn.close()

    return bookings