from backend.DB import connectDB


def load_summary():
    patients = count_patients()
    appointments = todays_appointments()
    payments = pending_payments()
    treatments = completed_treatments()
    
    data = [patients, appointments, payments, treatments]
    return data

def count_patients():
    patients = 0
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Patient")
    result = cursor.fetchone()
    if result:
        patients = result[0]
    cursor.close()
    conn.close()
    print("Total Patients:", patients)
    return str(patients)


def todays_appointments():
    appointments = 0
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Appointment 
        WHERE DATE(Schedule) = CURDATE()
          AND Status = 'Scheduled'
    """)
    result = cursor.fetchone()
    if result:
        appointments = result[0]
    cursor.close()
    conn.close()
    print("Today's Appointments:", appointments)
    return str(appointments)


def pending_payments():
    unpaid_payments = 0
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Pays 
        WHERE Payment_Status = 'Unpaid'
    """)
    result = cursor.fetchone()
    if result:
        unpaid_payments = result[0]
    cursor.close()
    conn.close()
    print("Pending Payments:", unpaid_payments)
    return str(unpaid_payments)


def completed_treatments():
    treatments_completed = 0
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Treatment 
        WHERE Treatment_Status = 'Completed'
    """)
    result = cursor.fetchone()
    if result:
        treatments_completed = result[0]
    cursor.close()
    conn.close()
    print("Completed Treatments:", treatments_completed)
    return str(treatments_completed)

def get_todays_appointments():
    todays_appointments = []

    conn = connectDB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            a.Appointment_ID,
            CONCAT(p.First_Name, ' ', p.Middle_Name, ' ', p.Last_Name) AS Patient_Full_Name,
            TIME(t.Treatment_Date_Time) AS Treatment_Time,
            t.Treatment_Procedure,
            t.Treatment_Status
        FROM Appointment a
        JOIN Patient p ON a.Patient_ID = p.Patient_ID
        LEFT JOIN Treatment t ON a.Appointment_ID = t.Appointment_ID
        WHERE DATE(a.Schedule) = CURDATE()
          AND a.Status = 'Scheduled'
    """)
    
    result = cursor.fetchall()
    if result:
        for row in result:
            todays_appointments.append(row)

    cursor.close()
    conn.close()
    
    print(todays_appointments)
    return todays_appointments

from backend.DB import connectDB


def get_todays_appointment_status_counts():
    conn = connectDB()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Status, COUNT(*) 
        FROM Appointment 
        WHERE DATE(Schedule) = CURDATE()
        GROUP BY Status
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Set default values
    scheduled = 0
    completed = 0
    cancelled = 0

    for status, count in results:
        if status == "Scheduled":
            scheduled = count
        elif status == "Completed":
            completed = count
        elif status == "Cancelled":
            cancelled = count

    return [scheduled, completed, cancelled]
