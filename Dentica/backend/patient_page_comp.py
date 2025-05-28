from backend.DB import connectDB
from mysql.connector import Error

def get_all_patient_records(patient_id):
    conn = connectDB()
    cursor = conn.cursor()
    patient_data = {}

    # Basic Patient Info
    cursor.execute("""
        SELECT 
            Patient_ID,
            CONCAT(First_Name, ' ', Middle_Name, ' ', Last_Name) AS Full_Name,
            Gender,
            Birth_Date,
            Contact_Number,
            Email,
            Address
        FROM Patient
        WHERE Patient_ID = %s
    """, (patient_id,))
    patient_data["info"] = cursor.fetchone()

    # Appointments
    cursor.execute("""
        SELECT 
            Appointment_ID,
            Schedule,
            Status
        FROM Appointment
        WHERE Patient_ID = %s
    """, (patient_id,))
    patient_data["appointments"] = cursor.fetchall()

    # Bookings
    cursor.execute("""
        SELECT 
            Booking_ID,
            Appointment_ID,
            Booking_Date_Time
        FROM Books
        WHERE Patient_ID = %s
    """, (patient_id,))
    patient_data["bookings"] = cursor.fetchall()

    # Cancellations
    cursor.execute("""
        SELECT 
            Appointment_ID,
            Cancellation_Date_Time,
            Reason
        FROM Cancel
        WHERE Patient_ID = %s
    """, (patient_id,))
    patient_data["cancellations"] = cursor.fetchall()

    # Payments
    cursor.execute("""
        SELECT 
            Payment_ID,
            Appointment_ID,
            Total_Amount,
            Payment_Method,
            Payment_Status
        FROM Pays
        WHERE Patient_ID = %s
    """, (patient_id,))
    patient_data["payments"] = cursor.fetchall()

    # Treatments (linked via Appointment_IDs)
    cursor.execute("""
        SELECT 
            T.Appointment_ID,
            T.Treatment_ID,
            T.Diagnosis,
            T.Cost,
            T.Treatment_Procedure,
            T.Treatment_Date_Time,
            T.Treatment_Status
        FROM Treatment T
        JOIN Appointment A ON T.Appointment_ID = A.Appointment_ID
        WHERE A.Patient_ID = %s
    """, (patient_id,))
    patient_data["treatments"] = cursor.fetchall()

    cursor.close()
    conn.close()
    return patient_data



def get_patients_appointment(patient_id):
    try:
        conn = connectDB()
        cursor = conn.cursor()

        query = """
        SELECT 
            a.Appointment_ID,
            a.Schedule,
            a.Status,
            COUNT(t.Treatment_ID) AS Treatment_Count,
            IFNULL(SUM(CASE 
                WHEN t.Treatment_Status != 'Canceled' THEN t.Cost 
                ELSE 0 
            END), 0) AS Total_Cost,
            IFNULL(p.Payment_Status, 'Unpaid') AS Payment_Status
        FROM Appointment a
        LEFT JOIN Treatment t ON a.Appointment_ID = t.Appointment_ID
        LEFT JOIN Pays p ON a.Appointment_ID = p.Appointment_ID AND a.Patient_ID = p.Patient_ID
        WHERE a.Patient_ID = %s
        GROUP BY a.Appointment_ID, a.Schedule, a.Status, p.Payment_Status
        ORDER BY a.Schedule DESC
        """

        cursor.execute(query, (patient_id,))
        rows = cursor.fetchall()

        appointments = []
        for row in rows:
            appointments.append({
                "Appointment_ID": row[0],
                "Schedule": row[1].strftime("%Y-%m-%d %H:%M:%S"),
                "Status": row[2],
                "Treatment_Count": row[3],
                "Total_Cost": float(row[4]),
                "Payment_Status": row[5]
            })

        return appointments

    except Error as e:
        print(f"MySQL error: {e}")
        return []

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
