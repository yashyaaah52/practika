from database.db_manager import get_connection

def get_financial_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(TotalCost), SUM(penaltyAmount) FROM Rentals")
    result = cursor.fetchone()
    conn.close()
    return {
        "revenue": result[0] if result[0] else 0.0,
        "penalties": result[1] if result[1] else 0.0
    }

def get_equipment_status_report():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM Equipment GROUP BY status")
    stats = cursor.fetchall()
    conn.close()
    return stats