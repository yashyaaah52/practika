from database.db_manager import get_connection

class Client:
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

def get_all_clients():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ClientID, Fullname, PassportData, Phone, Reliability FROM Client")
    rows = cursor.fetchall()
    conn.close()
    return [Client(*row) for row in rows]