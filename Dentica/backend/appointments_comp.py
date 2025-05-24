from backend.DB import connectDB


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
        SELECT Appointment_ID 
        FROM Appointment 
        ORDER BY CAST(SUBSTRING(Appointment_ID, 2) AS UNSIGNED) DESC 
        LIMIT 1
    """)

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        last_id = int(result[0][1:])  # Remove the 'A' and convert the number part
        new_id_num = last_id + 1
    else:
        new_id_num = 1  # Start from 1 if there are no appointments yet

    new_appointment_id = f'A{new_id_num:05d}'  # Zero-padded to 5 digits
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



def update_appointment_in_db(appointment_data):
    conn = connectDB()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        # Update appointment
        cursor.execute("""
            UPDATE Appointment SET
                Patient_ID = %s,
                Schedule = %s,
                Status = %s
            WHERE Appointment_ID = %s
        """, (
            appointment_data['Patient_ID'],
            appointment_data['Schedule'],
            appointment_data['Status'],
            appointment_data['Appointment_ID']
        ))

        # Delete existing treatments
        cursor.execute("""
            DELETE FROM Treatment
            WHERE Appointment_ID = %s
        """, (appointment_data['Appointment_ID'],))

        # Insert updated treatments
        for treatment in appointment_data['Treatments']:
            cursor.execute("""
                INSERT INTO Treatment (Appointment_ID, Treatment_ID, Diagnosis, Cost, Treatment_Procedure, Treatment_Date_Time, Treatment_Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                appointment_data['Appointment_ID'], treatment['Treatment_ID'],
                treatment["Diagnosis"], treatment["Cost"],
                treatment["Treatment_Procedure"], treatment["Treatment_Date_Time"],
                treatment["Treatment_Status"]
            ))

        # Update payment total_amount
        if 'Payment' in appointment_data and 'Total_Amount' in appointment_data['Payment']:
            cursor.execute("""
                UPDATE Pays SET
                    Total_Amount = %s
                WHERE Appointment_ID = %s
            """, (
                appointment_data['Payment']['Total_Amount'],
                appointment_data['Appointment_ID']
            ))

        conn.commit()
        return True

    except Exception as e:
        print("Error updating appointment:", e)
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
