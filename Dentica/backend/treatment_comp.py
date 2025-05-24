from backend.DB import connectDB

def delete_treatment_by_id(appointment_id, treatment_id):
    try:
        conn = connectDB()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Treatment
            WHERE Appointment_ID = %s AND Treatment_ID = %s
        """, (appointment_id, treatment_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[DB ERROR] Failed to delete treatment: {e}")
        return False
