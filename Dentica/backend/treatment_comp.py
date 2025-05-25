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
    
from PyQt6.QtWidgets import QMessageBox

def update_treatment(self, appointment_id, treatment_id, new_status):
    """
    Updates the Treatment_Status of a treatment record based on Appointment_ID and Treatment_ID.

    Args:
        appointment_id (str): The ID of the appointment.
        treatment_id (str): The ID of the treatment.
        new_status (str): New status to set. Example: 'In-Progress', 'Completed', etc.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = connectDB()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE Treatment
            SET Treatment_Status = %s
            WHERE Appointment_ID = %s AND Treatment_ID = %s
        """, (new_status, appointment_id, treatment_id))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Success", f"Successfully updated Treatment {treatment_id} (Appointment {appointment_id}) to '{new_status}'.")
            return True
        else:
            QMessageBox.warning(self, "Update Failed", f"No treatment record found for Appointment {appointment_id} and Treatment {treatment_id}.")
            return False
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Error updating treatment: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

