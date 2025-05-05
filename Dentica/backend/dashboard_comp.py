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

