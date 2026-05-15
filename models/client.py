"""Модуль работы с клиентами."""
from database.db_manager import get_connection


class Client:
    """Класс клиент."""
    def __init__(self, client_id=None, name=None, passport=None, phone=None, reliability="Высокая"):
        self.id = client_id
        self.name = name
        self.passport = passport
        self.phone = phone
        self.reliability = reliability

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:

            cursor.execute("""
                INSERT INTO Client (Fullname, PassportData, Phone, Reliability)
                VALUES (?, ?, ?, ?)
            """, (self.name, self.passport, self.phone, self.reliability))
            self.id = cursor.lastrowid
        else:

            cursor.execute("""
                UPDATE Client SET Fullname = ?, PassportData = ?, Phone = ?, Reliability = ?
                WHERE ClientID = ?
            """, (self.name, self.passport, self.phone, self.reliability, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет клиента из базы данных"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Client WHERE ClientID = ?", (self.id,))
            conn.commit()
            conn.close()


def get_all_client():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ClientID, Fullname, PassportData, Phone, Reliability FROM Client")
    rows = cursor.fetchall()
    conn.close()
    return [Client(*row) for row in rows]


def get_client_by_id(client_id):
    """Находит конкретного клиента по айди"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ClientID, FullName, PassportData, Phone, Reliability
        FROM Client
        WHERE ClientID = ?
    """, (client_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Client(client_id=row[0],
                      name=row[1],
                      passport=row[2],
                      phone=row[3],
                      reliability=row[4]
                      )
    return None
