from backend.DB import connectDB
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from decimal import Decimal, InvalidOperation



def get_all_appointments_with_treatment_count():
    all_appointments = []

    conn = connectDB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.Appointment_ID,
            CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Full_Name,
            DATE(a.Schedule) AS Appointment_Date,
            a.Status,
            COUNT(t.Treatment_ID) AS Treatment_Count
        FROM Appointment a
        JOIN Patient p ON a.Patient_ID = p.Patient_ID
        LEFT JOIN Treatment t ON a.Appointment_ID = t.Appointment_ID
        GROUP BY a.Appointment_ID, Patient_Full_Name, Appointment_Date, a.Status
        ORDER BY a.Schedule DESC
    """)
    
    result = cursor.fetchall()
    if result:
        for row in result:
            all_appointments.append(row)

    cursor.close()
    conn.close()
    
    return all_appointments

def generate_new_appointment_id():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT CAST(SUBSTRING(Appointment_ID, 2) AS UNSIGNED) AS num_id
        FROM Appointment
        ORDER BY num_id
    """)

    existing_ids = cursor.fetchall()
    cursor.close()
    conn.close()

    # Extract numeric parts into a set
    existing_id_set = set(num_id for (num_id,) in existing_ids)

    # Find the smallest missing positive integer
    expected_id = 1
    while expected_id in existing_id_set:
        expected_id += 1

    new_appointment_id = f'A{expected_id:05d}'  # e.g., A00002
    return new_appointment_id



def get_appointment_data(appointment_id):
    """Get complete appointment data including patient, treatments, booking, and payment"""
    conn = connectDB()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)

        # Get appointment and patient details
        cursor.execute("""
            SELECT a.Appointment_ID, a.Patient_ID, a.Schedule, a.Status,
                   CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Name
            FROM Appointment a
            JOIN Patient p ON a.Patient_ID = p.Patient_ID
            WHERE a.Appointment_ID = %s
        """, (appointment_id,))
        appointment = cursor.fetchone()

        if not appointment:
            return None

        if hasattr(appointment['Schedule'], 'strftime'):
            appointment['Schedule'] = appointment['Schedule'].strftime('%Y-%m-%d %H:%M:%S')

        # Get treatment records
        cursor.execute("""
            SELECT Treatment_ID, Diagnosis, Cost, Treatment_Procedure, 
                   Treatment_Date_Time, Treatment_Status
            FROM Treatment
            WHERE Appointment_ID = %s
            ORDER BY Treatment_ID ASC
        """, (appointment_id,))
        treatments = cursor.fetchall()
        for t in treatments:
            if hasattr(t['Treatment_Date_Time'], 'strftime'):
                t['Treatment_Date_Time'] = t['Treatment_Date_Time'].strftime('%Y-%m-%d %H:%M:%S')
        appointment['Treatments'] = treatments or []

        # Get booking info
        cursor.execute("""
            SELECT Booking_ID, Booking_Date_Time
            FROM Books
            WHERE Appointment_ID = %s
        """, (appointment_id,))
        booking = cursor.fetchone()
        if booking and hasattr(booking['Booking_Date_Time'], 'strftime'):
            booking['Booking_Date_Time'] = booking['Booking_Date_Time'].strftime('%Y-%m-%d %H:%M:%S')
        appointment['Booking'] = booking or {}

        # Get payment info
        cursor.execute("""
            SELECT Payment_ID, Total_Amount, Payment_Method, Payment_Status, Payment_Date
            FROM Pays
            WHERE Appointment_ID = %s
        """, (appointment_id,))
        payment = cursor.fetchone()
        appointment['Payment'] = payment or {}

        return appointment

    except Exception as e:
        print("Error getting appointment data:", e)
        return None

    finally:
        cursor.close()
        conn.close()

def update_appointment_in_db(self, appointment_data):
    """
    appointment_data must include:
      - Appointment_ID (str)
      - Patient_ID     (str)
      - Schedule       (str or datetime)
      - Status         ('Scheduled'|'Completed'|'Cancelled')
      - Treatments     (list of dicts)
      - Booking        (dict) ⏎ only for re-schedules:
          {
            "Booking_ID": str,
            "Patient_ID": str,
            "Appointment_ID": str,
            "Booking_Date_Time": str
          }
      - Payment        (dict) ⏎ only for re-schedules or updates:
          {
            "Payment_ID": str,
            "Patient_ID": str,
            "Appointment_ID": str,
            "Total_Amount": Decimal,
            "Payment_Method": str,
            "Payment_Status": str,
            "Payment_Date": str or None
          }
      - Cancel         (dict) ⏎ only when Status == 'Cancelled'
          {
            "Cancellation_Date_Time": str,
            "Reason": str
          }
    """
    conn = connectDB()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        appt_id = appointment_data["Appointment_ID"]
        pat_id  = appointment_data["Patient_ID"]
        status  = appointment_data["Status"]
        sched   = appointment_data["Schedule"]

        # 1) Update Appointment
        cursor.execute("""
            UPDATE Appointment
               SET Patient_ID = %s,
                   Schedule   = %s,
                   Status     = %s
             WHERE Appointment_ID = %s
        """, (pat_id, sched, status, appt_id))

        #check if the appointment is already paid if the status set to completed
        if status == "Completed":
            payment = appointment_data.get("Payment")
            if not payment or payment.get("Payment_Status") != "Paid":
                QMessageBox.warning(
                    self,
                    "Payment Required",
                    "Cannot mark appointment as 'Completed' while payment is 'Unpaid'."
                )
                conn.rollback()
                return False

            
        # 2) Books & Pays handling
        if status == "Cancelled":
            # a) Remove any existing booking & payment
            cursor.execute("DELETE FROM Pays  WHERE Appointment_ID = %s", (appt_id,))
            cursor.execute("DELETE FROM Books WHERE Appointment_ID = %s", (appt_id,))

        elif status == "Scheduled" and "Booking" in appointment_data and "Payment" in appointment_data:
            # b) Re-schedule: insert new booking + payment
            b = appointment_data["Booking"]
            p = appointment_data["Payment"]

            cursor.execute("""
                INSERT INTO Books (
                    Booking_ID, Patient_ID, Appointment_ID, Booking_Date_Time
                ) VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Booking_Date_Time = VALUES(Booking_Date_Time)
            """, (
                b["Booking_ID"],
                b["Patient_ID"],
                b["Appointment_ID"],
                b["Booking_Date_Time"]
            ))

            cursor.execute("""
                INSERT INTO Pays (
                    Payment_ID, Patient_ID, Appointment_ID,
                    Total_Amount, Payment_Method, Payment_Status, Payment_Date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Total_Amount   = VALUES(Total_Amount),
                    Payment_Method = VALUES(Payment_Method),
                    Payment_Status = VALUES(Payment_Status),
                    Payment_Date   = VALUES(Payment_Date)
            """, (
                p["Payment_ID"],
                p["Patient_ID"],
                p["Appointment_ID"],
                p["Total_Amount"],
                p["Payment_Method"],
                p["Payment_Status"],
                p.get("Payment_Date")
            ))

        else:
            # c) Normal Scheduled/Completed → bump booking timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                UPDATE Books
                   SET Booking_Date_Time = %s
                 WHERE Appointment_ID   = %s
            """, (now, appt_id))

     # 3) Refresh Treatments
        cursor.execute("DELETE FROM Treatment WHERE Appointment_ID = %s", (appt_id,))

        total_amount = Decimal("0.00") # This will store the sum minus canceled treatment costs

        for t in appointment_data["Treatments"]:
            cost = t["Cost"]

            # Determine final treatment status
            if t.get("Treatment_Status") == "Canceled":
                child_stat = "Canceled"
            else:
                if status == "Cancelled":
                    child_stat = "Canceled"
                elif status == "Scheduled":
                    child_stat = "Waiting"
                elif status == "Completed":
                    child_stat = "Completed"
           
            # Add cost only if treatment is not canceled
            if child_stat != "Canceled":
                try:
                    cost_decimal = Decimal(str(t["Cost"]))  # Safely convert cost
                    total_amount += cost_decimal
                except (InvalidOperation, KeyError, TypeError):
                    print("Invalid cost value:", t.get("Cost"))
                    # Handle or skip invalid cost entries if necessary
                    

            # Insert the treatment record
            cursor.execute("""
                INSERT INTO Treatment (
                    Appointment_ID, Treatment_ID, Diagnosis, Cost,
                    Treatment_Procedure, Treatment_Date_Time, Treatment_Status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                appt_id,
                t["Treatment_ID"],
                t["Diagnosis"],
                cost,
                t["Treatment_Procedure"],
                t["Treatment_Date_Time"],
                child_stat
            ))

        # 4) Upsert payment on Scheduled/Completed
        if status in ("Scheduled", "Completed") and "Payment" in appointment_data:
            p = appointment_data["Payment"]

            cursor.execute("""
                INSERT INTO Pays (
                    Payment_ID, Patient_ID, Appointment_ID,
                    Total_Amount, Payment_Method, Payment_Status, Payment_Date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Total_Amount   = VALUES(Total_Amount),
                    Payment_Method = VALUES(Payment_Method),
                    Payment_Status = VALUES(Payment_Status),
                    Payment_Date   = VALUES(Payment_Date)
            """, (
                p["Payment_ID"],
                p["Patient_ID"],
                p["Appointment_ID"],
                total_amount,  # Updated dynamic value
                p["Payment_Method"],
                p["Payment_Status"],
                p.get("Payment_Date")
            ))



        # 5) Cancel table
        if status == "Cancelled" and "Cancel" in appointment_data:
            c = appointment_data["Cancel"]
            # delete old
            cursor.execute("""
                DELETE FROM Cancel
                WHERE Appointment_ID = %s
            """, (appt_id,))
            # insert new
            cursor.execute("""
                INSERT INTO Cancel (
                    Patient_ID, Appointment_ID,
                    Cancellation_Date_Time, Reason
                ) VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Cancellation_Date_Time = VALUES(Cancellation_Date_Time),
                    Reason = VALUES(Reason)
            """, (
                pat_id, appt_id,
                c["Cancellation_Date_Time"],
                c["Reason"]
            ))
        elif status in ("Scheduled", "Completed"):
            # remove any stale cancellation
            cursor.execute("""
                DELETE FROM Cancel
                WHERE Patient_ID     = %s
                  AND Appointment_ID = %s
            """, (pat_id, appt_id))

        conn.commit()
        return True

    except Exception as e:
        QMessageBox.critical(self, "Database Error", f"{e}.")

        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()





# Function to search patients by name
# This function searches for patients by their first, middle, or last name.
# It returns a list of dictionaries containing the Patient_ID and Full_Name of matched patients.
# The search is case-insensitive and uses wildcards to match any part of the name.
def get_patients_name():
    matched_patients = []

    conn = connectDB()
    cursor = conn.cursor()

    query = """
        SELECT 
            Patient_ID,
            CONCAT(First_Name, ' ', Middle_Name, ' ', Last_Name) AS Full_Name
        FROM Patient
    """
    cursor.execute(query)

    result = cursor.fetchall()
    if result:
        for row in result:
            matched_patients.append({
                "Patient_ID": row[0],
                "Full_Name": row[1]
            })

    cursor.close()
    conn.close()

    return matched_patients













def save_appointment_to_db(appointment_data):
    conn = connectDB()
    cursor = conn.cursor()

    try:
        # Insert into Appointment
        cursor.execute("""
            INSERT INTO Appointment (Appointment_ID, Patient_ID, Schedule, Status)
            VALUES (%s, %s, %s, %s)
        """, (
            appointment_data["Appointment_ID"],
            appointment_data["Patient_ID"],
            appointment_data["Schedule"],
            appointment_data["Status"]
        ))

        # Insert Treatments
        for treatment in appointment_data["Treatments"]:
            cursor.execute("""
                INSERT INTO Treatment (
                    Appointment_ID, Treatment_ID, Diagnosis, Cost,
                    Treatment_Procedure, Treatment_Date_Time, Treatment_Status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                treatment["Appointment_ID"],
                treatment["Treatment_ID"],
                treatment["Diagnosis"],
                treatment["Cost"],
                treatment["Treatment_Procedure"],
                treatment["Treatment_Date_Time"],
                treatment["Treatment_Status"]
            ))

        # Insert into Books (Booking)
        cursor.execute("""
            INSERT INTO Books (Booking_ID, Patient_ID, Appointment_ID, Booking_Date_Time)
            VALUES (%s, %s, %s, %s)
        """, (
            appointment_data["Booking"]["Booking_ID"],
            appointment_data["Patient_ID"],
            appointment_data["Appointment_ID"],
            appointment_data["Booking"]["Booking_Date_Time"]
        ))

        # Insert into Pays (Payment)
        cursor.execute("""
            INSERT INTO Pays (
                Payment_ID, Patient_ID, Appointment_ID,
                Total_Amount, Payment_Method, Payment_Status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            appointment_data["Payment"]["Payment_ID"],
            appointment_data["Patient_ID"],
            appointment_data["Appointment_ID"],
            appointment_data["Payment"]["Total_Amount"],
            appointment_data["Payment"]["Payment_Method"],
            appointment_data["Payment"]["Payment_Status"]
            
        ))

        conn.commit()
        return True

    except Exception as e:
        print("Error saving appointment:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()

        

def perform_appointment_deletion(appointment_id):
    conn   = connectDB()
    cursor = conn.cursor()
    try:
        # 1) Delete all treatments for this appointment
        cursor.execute("""
            DELETE FROM Treatment
            WHERE Appointment_ID = %s
        """, (appointment_id,))

        # 2) Delete all bookings for this appointment
        cursor.execute("""
            DELETE FROM Books
            WHERE Appointment_ID = %s
        """, (appointment_id,))

        # 3) Delete all cancellations for this appointment
        cursor.execute("""
            DELETE FROM Cancel
            WHERE Appointment_ID = %s
        """, (appointment_id,))

        # 4) Delete all payments for this appointment
        cursor.execute("""
            DELETE FROM Pays
            WHERE Appointment_ID = %s
        """, (appointment_id,))

        # 5) Finally, delete the appointment itself
        cursor.execute("""
            DELETE FROM Appointment
            WHERE Appointment_ID = %s
        """, (appointment_id,))

        conn.commit()
        return True

    except Exception as e:
        print("Delete Appointment Error:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()



def search_appointments(keyword):
    conn   = connectDB()
    cursor = conn.cursor()

    # prepare the wildcarded keyword
    kw = keyword.lower()
    kw_like = f"%{kw}%"

    # aggregate treatments per appointment in a subquery, then filter all fields by LIKE
    query = """
    SELECT
      sub.Appointment_ID,
      sub.Patient_Full_Name,
      sub.Schedule,
      sub.Status,
      sub.Treatment_Count
    FROM (
      SELECT
        a.Appointment_ID,
        CONCAT(p.First_Name, ' ',
               p.Middle_Name, ' ',
               p.Last_Name)          AS Patient_Full_Name,
        a.Schedule,
        a.Status,
        COUNT(t.Treatment_ID)   AS Treatment_Count
      FROM Appointment a
      JOIN Patient p
        ON a.Patient_ID = p.Patient_ID
      LEFT JOIN Treatment t
        ON a.Appointment_ID = t.Appointment_ID
      GROUP BY
        a.Appointment_ID,
        Patient_Full_Name,
        a.Schedule,
        a.Status
    ) AS sub
    WHERE
      LOWER(sub.Patient_Full_Name) LIKE %s
      OR CAST(sub.Schedule AS CHAR)         LIKE %s
      OR LOWER(sub.Status)                  LIKE %s
      OR CAST(sub.Treatment_Count AS CHAR)  LIKE %s
    ORDER BY sub.Schedule
    """

    params = [kw_like, kw_like, kw_like, kw_like]

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # return list of lists: [Appointment_ID, Patient_Full_Name, Schedule, Status, Treatment_Count]
    return [list(r) for r in rows]

def get_appointment_details(appointment_id):
    conn = connectDB()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                a.Status, a.Schedule,
                b.Booking_ID, b.Booking_Date_Time,
                p.Payment_ID, p.Payment_Method, p.Payment_Status, p.Payment_Date
            FROM Appointment a
            LEFT JOIN Books b ON a.Appointment_ID = b.Appointment_ID
            LEFT JOIN Pays p ON a.Appointment_ID = p.Appointment_ID
            WHERE a.Appointment_ID = %s
        """, (appointment_id,))
        result = cursor.fetchone()
        if result:
            return {
                "Status":              result[0],
                "Schedule":            result[1],  # datetime
                "Booking_ID":          result[2],
                "Booking_Date_Time":   result[3],  # datetime
                "Payment_ID":          result[4],
                "Payment_Method":      result[5],
                "Payment_Status":      result[6],
                "Payment_Date":        result[7]   # Can be None
            }
        else:
            return None
    except Exception as e:
        print("Error fetching appointment details:", e)
        return None
    finally:
        cursor.close()
        conn.close()
