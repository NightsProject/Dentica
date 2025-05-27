from backend.DB import connectDB
from PyQt6.QtWidgets import QMessageBox

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
    

def update_treatment(self, appointment_id, treatment_id, new_status):
    """
    Updates the Treatment_Status of a treatment record based on Appointment_ID and Treatment_ID.

    Business Rules:
    - If trying to cancel a treatment but the appointment is already paid → block cancel.
    - If trying to start a treatment (In-Progress) but payment not made → block progress.

    Args:
        appointment_id (str): The ID of the appointment.
        treatment_id (str): The ID of the treatment.
        new_status (str): New status to set. Example: 'In-Progress', 'Completed', 'Canceled'.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = connectDB()
    cursor = conn.cursor()

    try:
        # Get payment status
        cursor.execute("""
            SELECT Payment_Status
            FROM Pays
            WHERE Appointment_ID = %s
        """, (appointment_id,))
        pay_row = cursor.fetchone()
        payment_status = pay_row[0] if pay_row else None

        # Rule 1: Cannot cancel paid treatment
        if new_status.lower() == "canceled" and payment_status == "Paid":
            QMessageBox.warning(
                self,
                "Cancellation Denied",
                f"Treatment cannot be canceled because payment for Appointment {appointment_id} is already marked as 'Paid'."
            )
            return False

        # Rule 2: Cannot proceed to In-Progress if not paid
        if new_status.lower() == "in-progress" and payment_status != "Paid":
            QMessageBox.warning(
                self,
                "Action Denied",
                f"Cannot proceed to 'In-Progress'. Payment for Appointment {appointment_id} is not yet completed."
            )
            return False

        # Proceed to update treatment status
        cursor.execute("""
            UPDATE Treatment
            SET Treatment_Status = %s
            WHERE Appointment_ID = %s AND Treatment_ID = %s
        """, (new_status, appointment_id, treatment_id))

        conn.commit()

        if cursor.rowcount > 0:
            QMessageBox.information(
                self,
                "Success",
                f"Successfully updated Treatment {treatment_id} (Appointment {appointment_id}) to '{new_status}'."
            )
            return True
        else:
            QMessageBox.warning(
                self,
                "Update Failed",
                f"No treatment record found for Appointment {appointment_id} and Treatment {treatment_id}."
            )
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
    is marked 'Completed' (excluding canceled ones), updates the Appointment.Status
    to 'Completed' and pops up a notification.

    Args:
        appointment_id (str): The appointment to check.
        parent (QWidget or None): Optional parent for the message box.

    Returns:
        bool: True if appointment was updated to Completed, False otherwise.
    """
    conn = connectDB()
    cursor = conn.cursor()

    try:
        # Count treatments that are neither Completed nor Canceled
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Treatment
            WHERE Appointment_ID = %s
              AND Treatment_Status NOT IN ('Completed', 'Canceled')
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
                        f"All active treatments for appointment {appointment_id} are completed.\n"
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


def auto_handle_all_treatments_canceled(appointment_id, parent=None):
    """
    Checks if all treatments for the given appointment are canceled.
    If yes, deletes or modifies the necessary data:
    - Marks appointment as 'Cancelled' (or deletes, depending on your design),
    - Removes bookings/payments,
    - Inserts cancellation data with a default reason,
    - Notifies user via QMessageBox if parent provided.

    Args:
        appointment_id (str): Appointment to check.
        parent (QWidget or None): For showing message boxes.

    Returns:
        bool: True if data was deleted/modified, False otherwise.
    """
    # Import datetime here or globally
    from datetime import datetime

    conn = connectDB()
    cursor = conn.cursor()

    try:
        # Check if all treatments are canceled
        cursor.execute("""
            SELECT COUNT(*)
            FROM Treatment
            WHERE Appointment_ID = %s
              AND Treatment_Status != 'Canceled'
        """, (appointment_id,))
        remaining = cursor.fetchone()[0]

        if remaining == 0:
            # All treatments canceled, proceed

            # Fetch current appointment details
            cursor.execute("""
                SELECT Status, Patient_ID
                FROM Appointment
                WHERE Appointment_ID = %s
            """, (appointment_id,))
            appt_row = cursor.fetchone()
            if not appt_row:
                return False  # appointment not found

            current_status, patient_id = appt_row

            if current_status == "Cancelled":
                # Already cancelled, no action
                return False

            # 1) Update appointment status to Cancelled
            cursor.execute("""
                UPDATE Appointment
                SET Status = 'Cancelled'
                WHERE Appointment_ID = %s
            """, (appointment_id,))

            # 2) Insert cancellation record with default reason
            cancel_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            default_reason = "Auto-cancelled because all treatments were cancelled."

            cursor.execute("""
                INSERT INTO Cancel (Patient_ID, Appointment_ID, Cancellation_Date_Time, Reason)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    Cancellation_Date_Time = VALUES(Cancellation_Date_Time),
                    Reason = VALUES(Reason)
            """, (patient_id, appointment_id, cancel_datetime, default_reason))

            # 3) Delete booking and payment records linked to this appointment
            cursor.execute("DELETE FROM Pays WHERE Appointment_ID = %s", (appointment_id,))
            cursor.execute("DELETE FROM Books WHERE Appointment_ID = %s", (appointment_id,))

            # 4) Commit changes
            conn.commit()

            # 5) Notify user
            if parent:
                QMessageBox.information(
                    parent,
                    "Appointment Auto-Cancelled",
                    f"Appointment {appointment_id} has been auto-cancelled "
                    "because all its treatments were cancelled."
                )

            return True

        else:
            # Not all treatments canceled, no action
            return False

    except Exception as e:
        print("Error in auto_handle_all_treatments_canceled:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


def update_total_amount_treatment_canceled(appointment_id, parent=None):
    """
    Recalculates the total amount for an appointment based on
    non-canceled treatments and updates the Payment record accordingly.

    Args:
        appointment_id (str): The appointment to update.
        parent (QWidget or None): Optional parent for message box.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    conn = connectDB()
    cursor = conn.cursor()

    try:
        # Get sum of all non-canceled treatment costs
        cursor.execute("""
            SELECT SUM(Cost)
            FROM Treatment
            WHERE Appointment_ID = %s
              AND Treatment_Status != 'Canceled'
        """, (appointment_id,))
        total = cursor.fetchone()[0] or 0.0

        # Update the Payment table
        cursor.execute("""
            UPDATE Pays
            SET Total_Amount = %s
            WHERE Appointment_ID = %s
        """, (total, appointment_id))

        conn.commit()

        if parent:
            QMessageBox.information(
                parent,
                "Payment Updated",
                f"The total payment amount has been updated to ₱{total:.2f} "
                f"after canceling one treatment."
            )

        return True

    except Exception as e:
        print("Error updating total amount:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()
