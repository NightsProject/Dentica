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


def check_treatment_completion(appointment_id, parent=None):
    """
    Checks all treatments for the given appointment_id. If every treatment
    is marked 'Completed', updates the Appointment.Status to 'Completed'
    and pops up a notification.

    Args:
        appointment_id (str): The appointment to check.
        parent (QWidget or None): Optional parent for the message box.

    Returns:
        bool: True if appointment was updated to Completed, False otherwise.
    """
    conn = connectDB()
    cursor = conn.cursor()

    try:
        # Count treatments not yet completed
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Treatment
            WHERE Appointment_ID = %s
              AND Treatment_Status != 'Completed'
        """, (appointment_id,))
        remaining = cursor.fetchone()[0]

        # If none remain, mark appointment as completed
        if remaining == 0:
            # First check current appointment status to avoid duplicate notifications
            cursor.execute("""
                SELECT Status 
                FROM Appointment
                WHERE Appointment_ID = %s
            """, (appointment_id,))
            current_status = cursor.fetchone()[0]

            if current_status != 'Completed':
                cursor.execute("""
                    UPDATE Appointment
                    SET Status = 'Completed'
                    WHERE Appointment_ID = %s
                """, (appointment_id,))
                conn.commit()

                # Notify user
                if parent:
                    QMessageBox.information(
                        parent,
                        "Appointment Completed",
                        f"All treatments for appointment {appointment_id} are done.\n"
                        "The appointment status has been set to Completed."
                    )
                return True

        return False

    except Exception as e:
        print("Error checking treatments:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()

    