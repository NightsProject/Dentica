from backend.DB import connectDB

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

#def get_patient_appointment(patient_id):